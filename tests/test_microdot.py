import sys
import unittest
from microdot import Microdot
from tests import mock_socket


class TestMicrodot(unittest.TestCase):
    def setUp(self):
        # mock socket module
        self.original_socket = sys.modules['microdot'].socket
        sys.modules['microdot'].socket = mock_socket

    def tearDown(self):
        # restore original socket module
        sys.modules['microdot'].socket = self.original_socket

    def test_get_request(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/')
        self.assertRaises(IndexError, app.run)
        self.assertEqual(fd.response, b'HTTP/1.0 200 OK\r\n'
                                      b'Content-Length: 3\r\n'
                                      b'Content-Type: text/plain\r\n'
                                      b'\r\n'
                                      b'foo')

    def test_post_request(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        @app.route('/', methods=['POST'])
        def index_post(req):
            return 'bar'

        mock_socket.clear_requests()
        fd = mock_socket.add_request('POST', '/')
        self.assertRaises(IndexError, app.run)
        self.assertEqual(fd.response, b'HTTP/1.0 200 OK\r\n'
                                      b'Content-Length: 3\r\n'
                                      b'Content-Type: text/plain\r\n'
                                      b'\r\n'
                                      b'bar')

    def test_404(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/foo')
        self.assertRaises(IndexError, app.run)
        self.assertEqual(fd.response, b'HTTP/1.0 404 N/A\r\n'
                                      b'Content-Length: 9\r\n'
                                      b'Content-Type: text/plain\r\n'
                                      b'\r\n'
                                      b'Not found')

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
        self.assertRaises(IndexError, app.run)
        self.assertEqual(fd.response, b'HTTP/1.0 200 OK\r\n'
                                      b'Content-Length: 3\r\n'
                                      b'Content-Type: text/plain\r\n'
                                      b'\r\n'
                                      b'404')

    def test_500(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 1 / 0

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/')
        self.assertRaises(IndexError, app.run)
        self.assertEqual(fd.response, b'HTTP/1.0 500 N/A\r\n'
                                      b'Content-Length: 21\r\n'
                                      b'Content-Type: text/plain\r\n'
                                      b'\r\n'
                                      b'Internal server error')

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
        self.assertEqual(fd.response, b'HTTP/1.0 501 N/A\r\n'
                                      b'Content-Length: 3\r\n'
                                      b'Content-Type: text/plain\r\n'
                                      b'\r\n'
                                      b'501')

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
        self.assertRaises(IndexError, app.run)
        self.assertEqual(fd.response, b'HTTP/1.0 501 N/A\r\n'
                                      b'Content-Length: 3\r\n'
                                      b'Content-Type: text/plain\r\n'
                                      b'\r\n'
                                      b'501')
