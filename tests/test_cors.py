import asyncio
import unittest
from microdot import Microdot
from microdot.test_client import TestClient
from microdot.cors import CORS


class TestCORS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.new_event_loop()

    def _run(self, coro):
        return self.loop.run_until_complete(coro)

    def test_origin(self):
        app = Microdot()
        cors = CORS(allowed_origins=['https://example.com'],
                    allow_credentials=True)
        cors.initialize(app)

        @app.get('/')
        def index(req):
            return 'foo'

        client = TestClient(app)
        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        self.assertFalse('Access-Control-Allow-Origin' in res.headers)
        self.assertFalse('Access-Control-Allow-Credentials' in res.headers)
        self.assertFalse('Vary' in res.headers)

        res = self._run(client.get(
            '/', headers={'Origin': 'https://example.com'}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Access-Control-Allow-Origin'],
                         'https://example.com')
        self.assertEqual(res.headers['Access-Control-Allow-Credentials'],
                         'true')
        self.assertEqual(res.headers['Vary'], 'Origin')

        cors.allow_credentials = False

        res = self._run(client.get(
            '/foo', headers={'Origin': 'https://example.com'}))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.headers['Access-Control-Allow-Origin'],
                         'https://example.com')
        self.assertFalse('Access-Control-Allow-Credentials' in res.headers)
        self.assertEqual(res.headers['Vary'], 'Origin')

        res = self._run(client.get('/', headers={'Origin': 'https://bad.com'}))
        self.assertEqual(res.status_code, 200)
        self.assertFalse('Access-Control-Allow-Origin' in res.headers)
        self.assertFalse('Access-Control-Allow-Credentials' in res.headers)
        self.assertFalse('Vary' in res.headers)

    def test_all_origins(self):
        app = Microdot()
        CORS(app, allowed_origins='*', expose_headers=['X-Test', 'X-Test2'])

        @app.get('/')
        def index(req):
            return 'foo'

        @app.get('/foo')
        def foo(req):
            return 'foo', {'Vary': 'X-Foo, X-Bar'}

        client = TestClient(app)
        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Access-Control-Allow-Origin'], '*')
        self.assertFalse('Vary' in res.headers)
        self.assertEqual(res.headers['Access-Control-Expose-Headers'],
                         'X-Test, X-Test2')

        res = self._run(client.get(
            '/', headers={'Origin': 'https://example.com'}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Access-Control-Allow-Origin'],
                         'https://example.com')
        self.assertEqual(res.headers['Vary'], 'Origin')
        self.assertEqual(res.headers['Access-Control-Expose-Headers'],
                         'X-Test, X-Test2')

        res = self._run(client.get(
            '/bad', headers={'Origin': 'https://example.com'}))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.headers['Access-Control-Allow-Origin'],
                         'https://example.com')
        self.assertEqual(res.headers['Vary'], 'Origin')
        self.assertEqual(res.headers['Access-Control-Expose-Headers'],
                         'X-Test, X-Test2')

        res = self._run(client.get(
            '/foo', headers={'Origin': 'https://example.com'}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Vary'], 'X-Foo, X-Bar, Origin')

    def test_cors_preflight(self):
        app = Microdot()
        CORS(app, allowed_origins='*')

        @app.route('/', methods=['GET', 'POST'])
        def index(req):
            return 'foo'

        client = TestClient(app)
        res = self._run(client.request('OPTIONS', '/', headers={
            'Origin': 'https://example.com',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'X-Test, X-Test2'}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Access-Control-Allow-Origin'],
                         'https://example.com')
        self.assertFalse('Access-Control-Max-Age' in res.headers)
        self.assertEqual(res.headers['Access-Control-Allow-Methods'], 'POST')
        self.assertEqual(res.headers['Access-Control-Allow-Headers'],
                         'X-Test, X-Test2')

        res = self._run(client.request('OPTIONS', '/', headers={
            'Origin': 'https://example.com'}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Access-Control-Allow-Origin'],
                         'https://example.com')
        self.assertFalse('Access-Control-Max-Age' in res.headers)
        self.assertFalse('Access-Control-Allow-Methods' in res.headers)
        self.assertFalse('Access-Control-Allow-Headers' in res.headers)

    def test_cors_preflight_with_options(self):
        app = Microdot()
        CORS(app, allowed_origins='*', max_age=3600, allowed_methods=['POST'],
             allowed_headers=['X-Test'])

        @app.route('/', methods=['GET', 'POST'])
        def index(req):
            return 'foo'

        client = TestClient(app)
        res = self._run(client.request('OPTIONS', '/', headers={
            'Origin': 'https://example.com',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'X-Test, X-Test2'}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Access-Control-Allow-Origin'],
                         'https://example.com')
        self.assertEqual(res.headers['Access-Control-Max-Age'], '3600')
        self.assertEqual(res.headers['Access-Control-Allow-Methods'], 'POST')
        self.assertEqual(res.headers['Access-Control-Allow-Headers'], 'X-Test')

        res = self._run(client.request('OPTIONS', '/', headers={
            'Origin': 'https://example.com',
            'Access-Control-Request-Method': 'GET'}))
        self.assertEqual(res.status_code, 200)
        self.assertFalse('Access-Control-Allow-Methods' in res.headers)
        self.assertFalse('Access-Control-Allow-Headers' in res.headers)

    def test_cors_disabled(self):
        app = Microdot()
        CORS(app, allowed_origins='*', handle_cors=False)

        @app.get('/')
        def index(req):
            return 'foo'

        client = TestClient(app)
        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        self.assertFalse('Access-Control-Allow-Origin' in res.headers)
        self.assertFalse('Vary' in res.headers)
