import sys
import unittest
from microdot import Microdot, Response, abort
from microdot_test_client import TestClient
from tests import mock_socket


class TestMicrodot(unittest.TestCase):
    def _mock(self):
        def mock_create_thread(f, *args, **kwargs):
            f(*args, **kwargs)

        self.original_socket = sys.modules['microdot'].socket
        self.original_create_thread = sys.modules['microdot'].create_thread
        sys.modules['microdot'].socket = mock_socket
        sys.modules['microdot'].create_thread = mock_create_thread

    def _unmock(self):
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

        client = TestClient(app)
        res = client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.headers['Content-Length'], '3')
        self.assertEqual(res.text, 'foo')
        self.assertEqual(res.body, b'foo')
        self.assertEqual(res.json, None)

    def test_post_request(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        @app.route('/', methods=['POST'])
        def index_post(req):
            return Response('bar')

        client = TestClient(app)
        res = client.post('/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.headers['Content-Length'], '3')
        self.assertEqual(res.text, 'bar')

    def test_head_request(self):
        self._mock()

        app = Microdot()

        @app.route('/foo')
        def index(req):
            return 'foo'

        mock_socket.clear_requests()
        fd = mock_socket.add_request('HEAD', '/foo')
        self._add_shutdown(app)
        app.run()

        self.assertTrue(fd.response.startswith(b'HTTP/1.0 200 OK\r\n'))
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain; charset=UTF-8\r\n',
                      fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\n'))

        self._unmock()

    def test_options_request(self):
        app = Microdot()

        @app.route('/', methods=['GET', 'DELETE'])
        def index(req):
            return 'foo'

        @app.post('/')
        def index_post(req):
            return 'bar'

        @app.route('/foo', methods=['POST', 'PUT'])
        def foo(req):
            return 'baz'

        client = TestClient(app)
        res = client.request('OPTIONS', '/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Allow'],
                         'GET, DELETE, POST, HEAD, OPTIONS')
        res = client.request('OPTIONS', '/foo')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Allow'], 'POST, PUT, OPTIONS')

    def test_empty_request(self):
        self._mock()

        app = Microdot()

        mock_socket.clear_requests()
        fd = mock_socket.FakeStream(b'\n')
        mock_socket._requests.append(fd)
        self._add_shutdown(app)
        app.run()
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 400 N/A\r\n'))
        self.assertIn(b'Content-Length: 11\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain; charset=UTF-8\r\n',
                      fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nBad request'))

        self._unmock()

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

        client = TestClient(app)
        methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        for method in methods:
            res = getattr(client, method.lower())('/' + method.lower())
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.headers['Content-Type'],
                             'text/plain; charset=UTF-8')
            self.assertEqual(res.text, method)

    def test_headers(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return req.headers.get('X-Foo')

        client = TestClient(app)
        res = client.get('/', headers={'X-Foo': 'bar'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'bar')

    def test_cookies(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return req.cookies['one'] + req.cookies['two'] + \
                req.cookies['three']

        client = TestClient(app, cookies={'one': '1', 'two': '2'})
        res = client.get('/', headers={'Cookie': 'three=3'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, '123')

    def test_binary_payload(self):
        app = Microdot()

        @app.post('/')
        def index(req):
            return req.body

        client = TestClient(app)
        res = client.post('/', body=b'foo')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'foo')

    def test_json_payload(self):
        app = Microdot()

        @app.post('/dict')
        def json_dict(req):
            print(req.headers)
            return req.json.get('foo')

        @app.post('/list')
        def json_list(req):
            return req.json[0]

        client = TestClient(app)

        res = client.post('/dict', body={'foo': 'bar'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'bar')

        res = client.post('/list', body=['foo', 'bar'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'foo')

    def test_tuple_responses(self):
        app = Microdot()

        @app.route('/body')
        def one(req):
            return 'one'

        @app.route('/body-status')
        def two(req):
            return 'two', 202

        @app.route('/body-headers')
        def three(req):
            return '<p>three</p>', {'Content-Type': 'text/html'}

        @app.route('/body-status-headers')
        def four(req):
            return '<p>four</p>', 202, \
                {'Content-Type': 'text/html; charset=UTF-8'}

        client = TestClient(app)

        res = client.get('/body')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'one')

        res = client.get('/body-status')
        self.assertEqual(res.status_code, 202)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'two')

        res = client.get('/body-headers')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'text/html')
        self.assertEqual(res.text, '<p>three</p>')

        res = client.get('/body-status-headers')
        self.assertEqual(res.status_code, 202)
        self.assertEqual(res.headers['Content-Type'],
                         'text/html; charset=UTF-8')
        self.assertEqual(res.text, '<p>four</p>')

    def test_before_after_request(self):
        app = Microdot()

        @app.before_request
        def before_request(req):
            if req.path == '/bar':
                @req.after_request
                def after_request(req, res):
                    res.headers['X-Two'] = '2'
                    return res
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

        client = TestClient(app)

        res = client.get('/bar')
        self.assertEqual(res.status_code, 202)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.headers['Set-Cookie'], ['foo=bar'])
        self.assertEqual(res.headers['X-One'], '1')
        self.assertEqual(res.headers['X-Two'], '2')
        self.assertEqual(res.text, 'bar')
        self.assertEqual(client.cookies['foo'], 'bar')

        res = client.get('/baz')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.headers['Set-Cookie'], ['foo=bar'])
        self.assertEqual(res.headers['X-One'], '1')
        self.assertFalse('X-Two' in res.headers)
        self.assertEqual(res.headers['Content-Length'], '3')
        self.assertEqual(res.text, 'baz')

    def test_after_error_request(self):
        app = Microdot()

        @app.after_error_request
        def after_error_request_one(req, res):
            res.headers['X-One'] = '1'

        @app.after_error_request
        def after_error_request_two(req, res):
            res.set_cookie('foo', 'bar')
            return res

        @app.route('/foo')
        def foo(req):
            return 'foo'

        client = TestClient(app)

        res = client.get('/foo')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertFalse('X-One' in res.headers)
        self.assertFalse('Set-Cookie' in res.headers)

        res = client.get('/bar')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.headers['Set-Cookie'], ['foo=bar'])
        self.assertEqual(res.headers['X-One'], '1')
        self.assertEqual(client.cookies['foo'], 'bar')

    def test_400(self):
        self._mock()

        app = Microdot()

        mock_socket.clear_requests()
        fd = mock_socket.FakeStream(b'\n')
        mock_socket._requests.append(fd)
        self._add_shutdown(app)
        app.run()
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 400 N/A\r\n'))
        self.assertIn(b'Content-Length: 11\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain; charset=UTF-8\r\n',
                      fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nBad request'))

        self._unmock()

    def test_400_handler(self):
        self._mock()

        app = Microdot()

        @app.errorhandler(400)
        def handle_400(req):
            return '400'

        mock_socket.clear_requests()
        fd = mock_socket.FakeStream(b'\n')
        mock_socket._requests.append(fd)
        self._add_shutdown(app)
        app.run()
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 200 OK\r\n'))
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain; charset=UTF-8\r\n',
                      fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\n400'))

        self._unmock()

    def test_404(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        client = TestClient(app)
        res = client.post('/foo')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'Not found')

    def test_404_handler(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        @app.errorhandler(404)
        def handle_404(req):
            return '404'

        client = TestClient(app)
        res = client.post('/foo')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, '404')

    def test_405(self):
        app = Microdot()

        @app.route('/foo')
        def index(req):
            return 'foo'

        client = TestClient(app)
        res = client.post('/foo')
        self.assertEqual(res.status_code, 405)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'Not found')

    def test_405_handler(self):
        app = Microdot()

        @app.route('/foo')
        def index(req):
            return 'foo'

        @app.errorhandler(405)
        def handle_405(req):
            return '405', 405

        client = TestClient(app)
        res = client.patch('/foo')
        self.assertEqual(res.status_code, 405)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, '405')

    def test_413(self):
        app = Microdot()

        @app.post('/')
        def index(req):
            return 'foo'

        client = TestClient(app)
        res = client.post('/foo', body='x' * 17000)
        self.assertEqual(res.status_code, 413)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'Payload too large')

    def test_413_handler(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        @app.errorhandler(413)
        def handle_413(req):
            return '413', 400

        client = TestClient(app)
        res = client.post('/foo', body='x' * 17000)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, '413')

    def test_500(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 1 / 0

        client = TestClient(app)
        res = client.get('/')
        self.assertEqual(res.status_code, 500)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'Internal server error')

    def test_500_handler(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 1 / 0

        @app.errorhandler(500)
        def handle_500(req):
            return '501', 501

        client = TestClient(app)
        res = client.get('/')
        self.assertEqual(res.status_code, 501)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, '501')

    def test_exception_handler(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 1 / 0

        @app.errorhandler(ZeroDivisionError)
        def handle_div_zero(req, exc):
            return '501', 501

        client = TestClient(app)
        res = client.get('/')
        self.assertEqual(res.status_code, 501)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, '501')

    def test_exception_handler_parent(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            foo = []
            return foo[1]

        @app.errorhandler(LookupError)
        def handle_lookup_error(req, exc):
            return exc.__class__.__name__, 501

        client = TestClient(app)
        res = client.get('/')
        self.assertEqual(res.status_code, 501)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'IndexError')

    def test_exception_handler_redundant_parent(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            foo = []
            return foo[1]

        @app.errorhandler(LookupError)
        def handle_lookup_error(req, exc):
            return 'LookupError', 501

        @app.errorhandler(IndexError)
        def handle_index_error(req, exc):
            return 'IndexError', 501

        client = TestClient(app)
        res = client.get('/')
        self.assertEqual(res.status_code, 501)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'IndexError')

    def test_exception_handler_multiple_parents(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            foo = []
            return foo[1]

        @app.errorhandler(Exception)
        def handle_generic_exception(req, exc):
            return 'Exception', 501

        @app.errorhandler(LookupError)
        def handle_lookup_error(req, exc):
            return 'LookupError', 501

        client = TestClient(app)
        res = client.get('/')
        self.assertEqual(res.status_code, 501)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'LookupError')

    def test_exception_handler_no_viable_parents(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            foo = []
            return foo[1]

        @app.errorhandler(RuntimeError)
        def handle_runtime_error(req, exc):
            return 'RuntimeError', 501

        client = TestClient(app)
        res = client.get('/')
        self.assertEqual(res.status_code, 500)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'Internal server error')

    def test_abort(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            abort(406, 'Not acceptable')
            return 'foo'

        client = TestClient(app)
        res = client.get('/')
        self.assertEqual(res.status_code, 406)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'Not acceptable')

    def test_abort_handler(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            abort(406)
            return 'foo'

        @app.errorhandler(406)
        def handle_406(req):
            return '406', 406

        client = TestClient(app)
        res = client.get('/')
        self.assertEqual(res.status_code, 406)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, '406')

    def test_json_response(self):
        app = Microdot()

        @app.route('/dict')
        def json_dict(req):
            return {'foo': 'bar'}

        @app.route('/list')
        def json_list(req):
            return ['foo', 'bar']

        client = TestClient(app)

        res = client.get('/dict')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'application/json; charset=UTF-8')
        self.assertEqual(res.json, {'foo': 'bar'})

        res = client.get('/list')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'application/json; charset=UTF-8')
        self.assertEqual(res.json, ['foo', 'bar'])

    def test_binary_response(self):
        app = Microdot()

        @app.route('/bin')
        def index(req):
            return b'\xff\xfe', {'Content-Type': 'application/octet-stream'}

        client = TestClient(app)
        res = client.get('/bin')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'application/octet-stream')
        self.assertEqual(res.text, None)
        self.assertEqual(res.json, None)
        self.assertEqual(res.body, b'\xff\xfe')

    def test_streaming(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            def stream():
                yield 'foo'
                yield b'bar'
            return stream()

        client = TestClient(app)
        res = client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'foobar')

    def test_already_handled_response(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return Response.already_handled

        client = TestClient(app)
        res = client.get('/')
        self.assertEqual(res, None)

    def test_mount(self):
        subapp = Microdot()

        @subapp.before_request
        def before(req):
            req.g.before = 'before'

        @subapp.after_request
        def after(req, res):
            res.body += b':after'

        @subapp.after_error_request
        def after_error(req, res):
            res.body += b':errorafter'

        @subapp.errorhandler(404)
        def not_found(req):
            return '404', 404

        @subapp.route('/app')
        def index(req):
            return req.g.before + ':foo'

        app = Microdot()
        app.mount(subapp, url_prefix='/sub')

        client = TestClient(app)

        res = client.get('/app')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, '404:errorafter')

        res = client.get('/sub/app')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'before:foo:after')

    def test_ssl(self):
        self._mock()

        app = Microdot()

        @app.route('/foo')
        def foo(req):
            return 'bar'

        class FakeSSL:
            def wrap_socket(self, sock, **kwargs):
                return sock

        mock_socket.clear_requests()
        fd = mock_socket.add_request('GET', '/foo')
        self._add_shutdown(app)
        app.run(ssl=FakeSSL())
        self.assertTrue(fd.response.startswith(b'HTTP/1.0 200 OK\r\n'))
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain; charset=UTF-8\r\n',
                      fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nbar'))

        self._unmock()
