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

from microdot_wsgi import Microdot, WSGIRequest


@unittest.skipIf(sys.implementation.name == 'micropython',
                 'not supported under MicroPython')
class TestMicrodotWSGI(unittest.TestCase):
    def test_wsgi_request_with_query_string(self):
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
        app = Microdot()
        req = WSGIRequest(app, environ)
        self.assertEqual(req.app, app)
        self.assertEqual(req.client_addr, ('1.2.3.4', 1234))
        self.assertEqual(req.method, 'POST')
        self.assertEqual(req.http_version, 'HTTP/1.1')
        self.assertEqual(req.path, '/foo/bar')
        self.assertEqual(req.args, {'baz': ['1']})
        self.assertEqual(req.cookies, {'session': 'xyz'})
        self.assertEqual(req.body, b'body')

    def test_wsgi_request_withiout_query_string(self):
        environ = {
            'SCRIPT_NAME': '/foo',
            'PATH_INFO': '/bar',
            'REMOTE_ADDR': '1.2.3.4',
            'REMOTE_PORT': '1234',
            'REQUEST_METHOD': 'GET',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.input': io.BytesIO(b''),
        }
        app = Microdot()
        req = WSGIRequest(app, environ)
        self.assertEqual(req.path, '/foo/bar')
        self.assertEqual(req.args, {})

    def test_wsgi_app(self):
        app = Microdot()

        @app.route('/foo')
        def foo(request):
            return 'bar'

        environ = {
            'PATH_INFO': '/foo',
            'REMOTE_ADDR': '1.2.3.4',
            'REMOTE_PORT': '1234',
            'REQUEST_METHOD': 'GET',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.input': io.BytesIO(b''),
        }

        def start_response(status, headers):
            self.assertEqual(status, '200 OK')
            self.assertEqual(headers, [('Content-Length', '3'),
                                       ('Content-Type', 'text/plain')])

        res = app(environ, start_response)
        body = b''
        for b in res:
            body += b
        self.assertEqual(body, b'bar')

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
