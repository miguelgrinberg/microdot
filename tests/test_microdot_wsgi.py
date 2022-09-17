import unittest
import sys

try:
    import uio as io
except ImportError:
    import io

try:
    from unittest import mock
except ImportError:
    mock = None

from microdot_wsgi import Microdot


@unittest.skipIf(sys.implementation.name == 'micropython',
                 'not supported under MicroPython')
class TestMicrodotWSGI(unittest.TestCase):
    def test_wsgi_request_with_query_string(self):
        app = Microdot()

        @app.post('/foo/bar')
        def index(req):
            self.assertEqual(req.app, app)
            self.assertEqual(req.client_addr, ('1.2.3.4', 1234))
            self.assertEqual(req.method, 'POST')
            self.assertEqual(req.http_version, 'HTTP/1.1')
            self.assertEqual(req.path, '/foo/bar')
            self.assertEqual(req.args, {'baz': ['1']})
            self.assertEqual(req.cookies, {'session': 'xyz'})
            self.assertEqual(req.body, b'body')
            return 'response'

        @app.after_request
        def after_request(req, resp):
            resp.set_cookie('foo', 'foo')
            resp.set_cookie('bar', 'bar', http_only=True)

        environ = {
            'SCRIPT_NAME': '/foo',
            'PATH_INFO': '/bar',
            'QUERY_STRING': 'baz=1',
            'HTTP_AUTHORIZATION': 'Bearer 123',
            'HTTP_COOKIE': 'session=xyz',
            'HTTP_CONTENT_LENGTH': '4',
            'REMOTE_ADDR': '1.2.3.4',
            'REMOTE_PORT': '1234',
            'REQUEST_METHOD': 'POST',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.input': io.BytesIO(b'body'),
        }

        def start_response(status, headers):
            self.assertEqual(status, '200 OK')
            expected_headers = [('Content-Length', '8'),
                                ('Content-Type', 'text/plain; charset=UTF-8'),
                                ('Set-Cookie', 'foo=foo'),
                                ('Set-Cookie', 'bar=bar; HttpOnly')]
            self.assertEqual(len(headers), len(expected_headers))
            for header in expected_headers:
                self.assertIn(header, headers)

        r = app(environ, start_response)
        self.assertEqual(next(r), b'response')

    def test_wsgi_request_without_query_string(self):
        app = Microdot()

        @app.route('/foo/bar')
        def index(req):
            self.assertEqual(req.path, '/foo/bar')
            self.assertEqual(req.args, {})
            return 'response'

        environ = {
            'SCRIPT_NAME': '/foo',
            'PATH_INFO': '/bar',
            'REMOTE_ADDR': '1.2.3.4',
            'REMOTE_PORT': '1234',
            'REQUEST_METHOD': 'GET',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.input': io.BytesIO(b''),
        }

        def start_response(status, headers):
            pass

        app(environ, start_response)

    def test_shutdown(self):
        app = Microdot()

        @app.route('/shutdown')
        def shutdown(request):
            request.app.shutdown()

        environ = {
            'PATH_INFO': '/shutdown',
            'REMOTE_ADDR': '1.2.3.4',
            'REMOTE_PORT': '1234',
            'REQUEST_METHOD': 'GET',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.input': io.BytesIO(b''),
        }

        def start_response(status, headers):
            pass

        with mock.patch('microdot_wsgi.os.kill') as kill:
            app(environ, start_response)

        kill.assert_called()
