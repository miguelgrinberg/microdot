import sys
import unittest
from microdot_asyncio import Microdot, Response
from tests import mock_asyncio, mock_socket


class TestMicrodotAsync(unittest.TestCase):
    def setUp(self):
        # mock socket module
        self.original_asyncio = sys.modules['microdot_asyncio'].asyncio
        sys.modules['microdot_asyncio'].asyncio = mock_asyncio

    def tearDown(self):
        # restore original socket module
        sys.modules['microdot_asyncio'].asyncio = self.original_asyncio

    def test_get_request(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        @app.route('/async')
        async def index2(req):
            return 'foo-async'

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/')
        fd2 = mock_socket.add_request('GET', '/async')
        self.assertRaises(IndexError, app.run)
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 200 OK\r\n'))
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nfoo'))
        self.assertTrue(fd2.response.startswith(b'HTTP/1.0 200 OK\r\n'))
        self.assertIn(b'Content-Length: 9\r\n', fd2.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd2.response)
        self.assertTrue(fd2.response.endswith(b'\r\n\r\nfoo-async'))

    def test_post_request(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        @app.route('/', methods=['POST'])
        def index_post(req):
            return Response('bar')

        @app.route('/async', methods=['POST'])
        async def index_post2(req):
            return Response('bar-async')

        mock_socket.clear_requests()
        fd = mock_socket.add_request('POST', '/')
        fd2 = mock_socket.add_request('POST', '/async')
        self.assertRaises(IndexError, app.run)
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 200 OK\r\n'))
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nbar'))
        self.assertTrue(fd2.response.startswith(b'HTTP/1.0 200 OK\r\n'))
        self.assertIn(b'Content-Length: 9\r\n', fd2.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd2.response)
        self.assertTrue(fd2.response.endswith(b'\r\n\r\nbar-async'))

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
        async def after_request_two(req, res):
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
        self.assertRaises(IndexError, app.run)
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 202 N/A\r\n'))
        self.assertIn(b'X-One: 1\r\n', fd.response)
        self.assertIn(b'Set-Cookie: foo=bar\r\n', fd.response)
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nbar'))

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/baz')
        self.assertRaises(IndexError, app.run)
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
        self.assertRaises(IndexError, app.run)
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
        async def handle_404(req):
            return '404'

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/foo')
        self.assertRaises(IndexError, app.run)
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 200 OK\r\n'))
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\n404'))

    def test_500(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 1 / 0

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/')
        self.assertRaises(IndexError, app.run)
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
        self.assertRaises(IndexError, app.run)
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
        async def handle_div_zero(req, exc):
            return '501', 501

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/')
        self.assertRaises(IndexError, app.run)
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 501 N/A\r\n'))
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\n501'))
