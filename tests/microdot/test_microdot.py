import sys
import unittest
from microdot import Microdot, Response
from tests import mock_socket


def mock_create_thread(f, *args, **kwargs):
    f(*args, **kwargs)


class TestMicrodot(unittest.TestCase):
    def setUp(self):
        # mock socket module
        self.original_socket = sys.modules['microdot'].socket
        self.original_create_thread = sys.modules['microdot'].create_thread
        sys.modules['microdot'].socket = mock_socket
        sys.modules['microdot'].create_thread = mock_create_thread

    def tearDown(self):
        # restore original socket module
        sys.modules['microdot'].socket = self.original_socket
        sys.modules['microdot'].create_thread = self.original_create_thread

    def _add_shutdown(self, app):
        @app.route('/shutdown')
        def shutdown(req):
            app.shutdown()
            return ''

        mock_socket.add_request('GET', '/shutdown')

    def test_get_request(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/')
        self._add_shutdown(app)
        app.run()
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 200 OK\r\n'))
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nfoo'))

    def test_post_request(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        @app.route('/', methods=['POST'])
        def index_post(req):
            return Response('bar')

        mock_socket.clear_requests()
        fd = mock_socket.add_request('POST', '/')
        self._add_shutdown(app)
        app.run()
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 200 OK\r\n'))
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nbar'))

    def test_empty_request(self):
        app = Microdot()

        mock_socket.clear_requests()
        fd = mock_socket.FakeStream(b'\n')
        mock_socket._requests.append(fd)
        self._add_shutdown(app)
        app.run()
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 400 N/A\r\n'))
        self.assertIn(b'Content-Length: 11\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nBad request'))

    def test_method_decorators(self):
        app = Microdot()

        @app.get('/get')
        def get(req):
            return 'GET'

        @app.post('/post')
        def post(req):
            return 'POST'

        @app.put('/put')
        def put(req):
            return 'PUT'

        @app.patch('/patch')
        def patch(req):
            return 'PATCH'

        @app.delete('/delete')
        def delete(req):
            return 'DELETE'

        methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        mock_socket.clear_requests()
        fds = [mock_socket.add_request(method, '/' + method.lower())
               for method in methods]
        self._add_shutdown(app)
        app.run()
        for fd, method in zip(fds, methods):
            self.assertTrue(fd.response.endswith(
                b'\r\n\r\n' + method.encode()))

    def test_before_after_request(self):
        app = Microdot()

        @app.before_request
        def before_request(req):
            if req.path == '/bar':
                return 'bar', 202
            req.g.message = 'baz'

        @app.after_request
        def after_request_one(req, res):
            res.headers['X-One'] = '1'

        @app.after_request
        def after_request_two(req, res):
            res.set_cookie('foo', 'bar')
            return res

        @app.route('/bar')
        def bar(req):
            return 'foo'

        @app.route('/baz')
        def baz(req):
            return req.g.message

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/bar')
        self._add_shutdown(app)
        app.run()
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 202 N/A\r\n'))
        self.assertIn(b'X-One: 1\r\n', fd.response)
        self.assertIn(b'Set-Cookie: foo=bar\r\n', fd.response)
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nbar'))

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/baz')
        self._add_shutdown(app)
        app.run()
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 200 OK\r\n'))
        self.assertIn(b'X-One: 1\r\n', fd.response)
        self.assertIn(b'Set-Cookie: foo=bar\r\n', fd.response)
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nbaz'))

    def test_404(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/foo')
        self._add_shutdown(app)
        app.run()
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 404 N/A\r\n'))
        self.assertIn(b'Content-Length: 9\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nNot found'))

    def test_404_handler(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        @app.errorhandler(404)
        def handle_404(req):
            return '404'

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/foo')
        self._add_shutdown(app)
        app.run()
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 200 OK\r\n'))
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\n404'))

    def test_413(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/foo', body='x' * 17000)
        self._add_shutdown(app)
        app.run()
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 413 N/A\r\n'))
        self.assertIn(b'Content-Length: 17\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nPayload too large'))

    def test_413_handler(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        @app.errorhandler(413)
        def handle_413(req):
            return '413', 400

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/foo', body='x' * 17000)
        self._add_shutdown(app)
        app.run()
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 400 N/A\r\n'))
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\n413'))

    def test_500(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 1 / 0

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/')
        self._add_shutdown(app)
        app.run()
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 500 N/A\r\n'))
        self.assertIn(b'Content-Length: 21\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nInternal server error'))

    def test_500_handler(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 1 / 0

        @app.errorhandler(500)
        def handle_500(req):
            return '501', 501

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/')
        self._add_shutdown(app)
        app.run()
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 501 N/A\r\n'))
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\n501'))

    def test_exception_handler(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 1 / 0

        @app.errorhandler(ZeroDivisionError)
        def handle_div_zero(req, exc):
            return '501', 501

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/')
        self._add_shutdown(app)
        app.run()
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 501 N/A\r\n'))
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\n501'))
