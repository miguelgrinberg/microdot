import asyncio
import unittest
from microdot import Microdot, Response, abort
from microdot.test_client import TestClient


class TestMicrodot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if hasattr(asyncio, 'set_event_loop'):
            asyncio.set_event_loop(asyncio.new_event_loop())
        cls.loop = asyncio.get_event_loop()

    def _run(self, coro):
        return self.loop.run_until_complete(coro)

    def test_get_request(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        @app.route('/async')
        async def index2(req):
            return 'foo-async'

        @app.route('/arg/<id>')
        def index3(req, id):
            return id

        @app.route('/arg/async/<id>')
        async def index4(req, id):
            return f'async-{id}'

        client = TestClient(app)

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.headers['Content-Length'], '3')
        self.assertEqual(res.text, 'foo')
        self.assertEqual(res.body, b'foo')
        self.assertEqual(res.json, None)

        res = self._run(client.get('/async'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.headers['Content-Length'], '9')
        self.assertEqual(res.text, 'foo-async')
        self.assertEqual(res.body, b'foo-async')
        self.assertEqual(res.json, None)

        res = self._run(client.get('/arg/123'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.headers['Content-Length'], '3')
        self.assertEqual(res.text, '123')
        self.assertEqual(res.body, b'123')
        self.assertEqual(res.json, None)

        res = self._run(client.get('/arg/async/123'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.headers['Content-Length'], '9')
        self.assertEqual(res.text, 'async-123')
        self.assertEqual(res.body, b'async-123')
        self.assertEqual(res.json, None)

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

        client = TestClient(app)

        res = self._run(client.post('/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.headers['Content-Length'], '3')
        self.assertEqual(res.text, 'bar')
        self.assertEqual(res.body, b'bar')
        self.assertEqual(res.json, None)

        res = self._run(client.post('/async'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.headers['Content-Length'], '9')
        self.assertEqual(res.text, 'bar-async')
        self.assertEqual(res.body, b'bar-async')
        self.assertEqual(res.json, None)

    def test_head_request(self):
        app = Microdot()

        @app.route('/foo')
        def index(req):
            return 'foo'

        client = TestClient(app)
        res = self._run(client.request('HEAD', '/foo'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.headers['Content-Length'], '3')
        self.assertIsNone(res.body)
        self.assertIsNone(res.text)
        self.assertIsNone(res.json)

    def test_options_request(self):
        app = Microdot()

        @app.route('/', methods=['GET', 'DELETE'])
        async def index(req):
            return 'foo'

        @app.post('/')
        async def index_post(req):
            return 'bar'

        @app.route('/foo', methods=['POST', 'PUT'])
        async def foo(req):
            return 'baz'

        client = TestClient(app)
        res = self._run(client.request('OPTIONS', '/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Allow'],
                         'GET, DELETE, POST, HEAD, OPTIONS')
        res = self._run(client.request('OPTIONS', '/foo'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Allow'], 'POST, PUT, OPTIONS')

    def test_method_decorators(self):
        app = Microdot()

        @app.get('/get')
        def get(req):
            return 'GET'

        @app.post('/post')
        async def post(req):
            return 'POST'

        @app.put('/put')
        def put(req):
            return 'PUT'

        @app.patch('/patch')
        async def patch(req):
            return 'PATCH'

        @app.delete('/delete')
        def delete(req):
            return 'DELETE'

        client = TestClient(app)
        methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        for method in methods:
            res = self._run(getattr(
                client, method.lower())('/' + method.lower()))
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
        res = self._run(client.get('/', headers={'X-Foo': 'bar'}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'bar')

    def test_cookies(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            res = Response(
                req.cookies['one'] + req.cookies['two'] + req.cookies['three'])
            res.set_cookie('four', '4')
            res.delete_cookie('two', path='/')
            res.delete_cookie('one', path='/bad')
            return res

        client = TestClient(app, cookies={'one': '1', 'two': '2'})
        res = self._run(client.get('/', headers={'Cookie': 'three=3'}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, '123')
        self.assertEqual(client.cookies, {'one': '1', 'four': '4'})

    def test_binary_payload(self):
        app = Microdot()

        @app.post('/')
        def index(req):
            return req.body

        client = TestClient(app)
        res = self._run(client.post('/', body=b'foo'))
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

        res = self._run(client.post('/dict', body={'foo': 'bar'}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'bar')

        res = self._run(client.post('/list', body=['foo', 'bar']))
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

        @app.route('/status')
        def five(req):
            return 202

        @app.route('/status-headers')
        def six(req):
            return 202, {'Content-Type': 'text/html; charset=UTF-8'}

        client = TestClient(app)

        res = self._run(client.get('/body'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'one')

        res = self._run(client.get('/body-status'))
        self.assertEqual(res.status_code, 202)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'two')

        res = self._run(client.get('/body-headers'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'text/html')
        self.assertEqual(res.text, '<p>three</p>')

        res = self._run(client.get('/body-status-headers'))
        self.assertEqual(res.status_code, 202)
        self.assertEqual(res.headers['Content-Type'],
                         'text/html; charset=UTF-8')
        self.assertEqual(res.text, '<p>four</p>')

        res = self._run(client.get('/status'))
        self.assertEqual(res.text, '')
        self.assertEqual(res.status_code, 202)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')

        res = self._run(client.get('/status-headers'))
        self.assertEqual(res.text, '')
        self.assertEqual(res.status_code, 202)
        self.assertEqual(res.headers['Content-Type'],
                         'text/html; charset=UTF-8')

    def test_before_after_request(self):
        app = Microdot()

        @app.before_request
        def before_request(req):
            if req.path == '/bar':
                @req.after_request
                async def after_request(req, res):
                    res.headers['X-Two'] = '2'
                    return res
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

        client = TestClient(app)

        res = self._run(client.get('/bar'))
        self.assertEqual(res.status_code, 202)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.headers['Set-Cookie'], ['foo=bar'])
        self.assertEqual(res.headers['X-One'], '1')
        self.assertEqual(res.headers['X-Two'], '2')
        self.assertEqual(res.text, 'bar')
        self.assertEqual(client.cookies['foo'], 'bar')

        res = self._run(client.get('/baz'))
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

        res = self._run(client.get('/foo'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertFalse('X-One' in res.headers)
        self.assertFalse('Set-Cookie' in res.headers)

        res = self._run(client.get('/bar'))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.headers['Set-Cookie'], ['foo=bar'])
        self.assertEqual(res.headers['X-One'], '1')
        self.assertEqual(client.cookies['foo'], 'bar')

    def test_400(self):
        app = Microdot()

        res = self._run(app.dispatch_request(None))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.body, b'Bad request')

    def test_400_handler(self):
        app = Microdot()

        @app.errorhandler(400)
        async def handle_400(req):
            return '400'

        res = self._run(app.dispatch_request(None))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.body, b'400')

    def test_404(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        client = TestClient(app)
        res = self._run(client.post('/foo'))
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
        async def handle_404(req):
            return '404'

        client = TestClient(app)
        res = self._run(client.post('/foo'))
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
        res = self._run(client.post('/foo'))
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
        async def handle_405(req):
            return '405', 405

        client = TestClient(app)
        res = self._run(client.patch('/foo'))
        self.assertEqual(res.status_code, 405)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, '405')

    def test_413(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return 'foo'

        client = TestClient(app)
        res = self._run(client.post('/foo', body='x' * 17000))
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
        async def handle_413(req):
            return '413', 400

        client = TestClient(app)
        res = self._run(client.post('/foo', body='x' * 17000))
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
        res = self._run(client.get('/'))
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
        res = self._run(client.get('/'))
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
        async def handle_div_zero(req, exc):
            return '501', 501

        client = TestClient(app)
        res = self._run(client.get('/'))
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
        async def handle_lookup_error(req, exc):
            return exc.__class__.__name__, 501

        client = TestClient(app)
        res = self._run(client.get('/'))
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
        async def handle_lookup_error(req, exc):
            return 'LookupError', 501

        @app.errorhandler(IndexError)
        async def handle_index_error(req, exc):
            return 'IndexError', 501

        client = TestClient(app)
        res = self._run(client.get('/'))
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
        async def handle_generic_exception(req, exc):
            return 'Exception', 501

        @app.errorhandler(LookupError)
        async def handle_lookup_error(req, exc):
            return 'LookupError', 501

        client = TestClient(app)
        res = self._run(client.get('/'))
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
        async def handle_runtime_error(req, exc):
            return 'RuntimeError', 501

        client = TestClient(app)
        res = self._run(client.get('/'))
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
        res = self._run(client.get('/'))
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
        def handle_500(req):
            return '406', 406

        client = TestClient(app)
        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 406)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, '406')

    def test_json_response(self):
        app = Microdot()

        @app.route('/dict')
        async def json_dict(req):
            return {'foo': 'bar'}

        @app.route('/list')
        def json_list(req):
            return ['foo', 'bar']

        client = TestClient(app)

        res = self._run(client.get('/dict'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'application/json; charset=UTF-8')
        self.assertEqual(res.json, {'foo': 'bar'})

        res = self._run(client.get('/list'))
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
        res = self._run(client.get('/bin'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'application/octet-stream')
        self.assertEqual(res.text, None)
        self.assertEqual(res.json, None)
        self.assertEqual(res.body, b'\xff\xfe')

    def test_streaming(self):
        app = Microdot()
        done = False

        @app.route('/')
        def index(req):
            class stream():
                def __init__(self):
                    self.i = 0
                    self.data = ['foo', b'bar']

                def __aiter__(self):
                    return self

                async def __anext__(self):
                    if self.i >= len(self.data):
                        raise StopAsyncIteration
                    data = self.data[self.i]
                    self.i += 1
                    return data

                async def aclose(self):
                    nonlocal done
                    done = True

            return stream()

        client = TestClient(app)
        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'foobar')
        self.assertEqual(done, True)

    def test_already_handled_response(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return Response.already_handled

        client = TestClient(app)
        res = self._run(client.get('/'))
        self.assertEqual(res.body, None)

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
            return req.g.before + ':' + req.url_prefix

        app = Microdot()
        app.mount(subapp, url_prefix='/sub')

        client = TestClient(app)

        res = self._run(client.get('/app'))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, '404:errorafter')

        res = self._run(client.get('/sub/app'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'before:/sub:after')

    def test_mount_local(self):
        subapp1 = Microdot()
        subapp2 = Microdot()

        @subapp1.before_request
        def before1(req):
            req.g.before += ':before1'

        @subapp1.after_error_request
        def after_error1(req, res):
            res.body += b':errorafter'

        @subapp1.errorhandler(ValueError)
        def value_error(req, exc):
            return str(exc), 400

        @subapp1.route('/')
        def index1(req):
            raise ZeroDivisionError()

        @subapp1.route('/foo')
        def foo(req):
            return req.g.before + ':foo:' + req.url_prefix

        @subapp1.route('/err')
        def err(req):
            raise ValueError('err')

        @subapp1.route('/err2')
        def err2(req):
            class MyErr(ValueError):
                pass

            raise MyErr('err')

        @subapp2.before_request
        def before2(req):
            req.g.before += ':before2'

        @subapp2.after_request
        def after2(req, res):
            res.body += b':after'

        @subapp2.errorhandler(405)
        def method_not_found2(req):
            return '405', 405

        @subapp2.route('/bar')
        def bar(req):
            return req.g.before + ':bar:' + req.url_prefix

        @subapp2.route('/baz')
        def baz(req):
            abort(405)

        app = Microdot()

        @app.before_request
        def before(req):
            req.g.before = 'before-app'

        @app.after_request
        def after(req, res):
            res.body += b':after-app'

        app.mount(subapp1, local=True)
        app.mount(subapp2, url_prefix='/sub', local=True)

        client = TestClient(app)

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 500)
        self.assertEqual(res.text, 'Internal server error:errorafter')

        res = self._run(client.get('/foo'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text, 'before-app:before1:foo::after-app')

        res = self._run(client.get('/err'))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.text, 'err:errorafter')

        res = self._run(client.get('/err2'))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.text, 'err:errorafter')

        res = self._run(client.get('/sub/bar'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        self.assertEqual(res.text,
                         'before-app:before2:bar:/sub:after:after-app')

        res = self._run(client.post('/sub/bar'))
        self.assertEqual(res.status_code, 405)
        self.assertEqual(res.text, '405')

        res = self._run(client.get('/sub/baz'))
        self.assertEqual(res.status_code, 405)
        self.assertEqual(res.text, '405')

    def test_many_mounts(self):
        subsubapp = Microdot()

        @subsubapp.before_request
        def subsubapp_before(req):
            req.g.before = 'subsubapp'

        @subsubapp.route('/')
        def subsubapp_index(req):
            return f'{req.g.before}:{req.subapp == subsubapp}:{req.url_prefix}'

        subapp = Microdot()

        @subapp.before_request
        def subapp_before(req):
            req.g.before = 'subapp'

        @subapp.route('/')
        def subapp_index(req):
            return f'{req.g.before}:{req.subapp == subapp}:{req.url_prefix}'

        app = Microdot()

        @app.before_request
        def app_before(req):
            req.g.before = 'app'

        @app.route('/')
        def app_index(req):
            return f'{req.g.before}:{req.subapp is None}:{req.url_prefix}'

        subapp.mount(subsubapp, url_prefix='/subsub')
        app.mount(subapp, url_prefix='/sub')

        client = TestClient(app)

        res = self._run(client.get('/sub/subsub/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'subsubapp:True:/sub/subsub')

        res = self._run(client.get('/sub/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'subsubapp:True:/sub')

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'subsubapp:True:')

    def test_many_local_mounts(self):
        subsubapp = Microdot()

        @subsubapp.before_request
        def subsubapp_before(req):
            req.g.before = 'subsubapp'

        @subsubapp.route('/')
        def subsubapp_index(req):
            return f'{req.g.before}:{req.subapp == subsubapp}:{req.url_prefix}'

        subapp = Microdot()

        @subapp.before_request
        def subapp_before(req):
            req.g.before = 'subapp'

        @subapp.route('/')
        def subapp_index(req):
            return f'{req.g.before}:{req.subapp == subapp}:{req.url_prefix}'

        app = Microdot()

        @app.before_request
        def app_before(req):
            req.g.before = 'app'

        @app.route('/')
        def app_index(req):
            return f'{req.g.before}:{req.subapp is None}:{req.url_prefix}'

        subapp.mount(subsubapp, url_prefix='/subsub', local=True)
        app.mount(subapp, url_prefix='/sub', local=True)

        client = TestClient(app)

        res = self._run(client.get('/sub/subsub/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'subsubapp:True:/sub/subsub')

        res = self._run(client.get('/sub/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'subapp:True:/sub')

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'app:True:')
