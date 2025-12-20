import asyncio
import unittest
from microdot import Microdot
from microdot.cors import CORS
from microdot.csrf import CSRF
from microdot.test_client import TestClient


class TestCSRF(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if hasattr(asyncio, 'set_event_loop'):
            asyncio.set_event_loop(asyncio.new_event_loop())
        cls.loop = asyncio.get_event_loop()

    def _run(self, coro):
        return self.loop.run_until_complete(coro)

    def test_protect_all_true(self):
        app = Microdot()
        csrf = CSRF(app)

        @app.get('/')
        def index(request):
            return 204

        @app.post('/submit')
        def submit(request):
            return 204

        @app.post('/submit-exempt')
        @csrf.exempt
        def submit_exempt(request):
            return 204

        @app.get('/get-protected')
        @csrf.protect
        def index(request):
            return 204

        client = TestClient(app)

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.get(
            '/', headers={'Sec-Fetch-Site': 'cross-site'}
        ))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.get(
            '/', headers={'Origin': 'https://evil.com'}
        ))
        self.assertEqual(res.status_code, 204)

        res = self._run(client.post('/submit'))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.post(
            '/submit', headers={'Sec-Fetch-Site': 'cross-site'}
        ))
        self.assertEqual(res.status_code, 403)
        res = self._run(client.post(
            '/submit', headers={'Sec-Fetch-Site': 'same-site'}
        ))
        self.assertEqual(res.status_code, 403)
        res = self._run(client.post(
            '/submit', headers={'Sec-Fetch-Site': 'same-origin'}
        ))
        self.assertEqual(res.status_code, 204)

        res = self._run(client.post('/submit-exempt'))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.post(
            '/submit-exempt', headers={'Sec-Fetch-Site': 'cross-site'}
        ))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.get('/get-protected'))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.get(
            '/get-protected', headers={'Sec-Fetch-Site': 'cross-site'}
        ))
        self.assertEqual(res.status_code, 403)

    def test_protect_all_false(self):
        app = Microdot()
        csrf = CSRF(protect_all=False)
        csrf.initialize(app)

        @app.get('/')
        def index(request):
            return 204

        @app.post('/submit')
        @csrf.protect
        def submit(request):
            return 204

        @app.post('/submit-exempt')
        def submit_exempt(request):
            return 204

        client = TestClient(app)

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.get(
            '/', headers={'Sec-Fetch-Site': 'cross-site'}
        ))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.get(
            '/', headers={'Origin': 'https://evil.com'}
        ))
        self.assertEqual(res.status_code, 204)

        res = self._run(client.post('/submit'))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.post(
            '/submit', headers={'Sec-Fetch-Site': 'cross-site'}
        ))
        self.assertEqual(res.status_code, 403)
        res = self._run(client.post(
            '/submit', headers={'Sec-Fetch-Site': 'same-site'}
        ))
        self.assertEqual(res.status_code, 403)
        res = self._run(client.post(
            '/submit', headers={'Sec-Fetch-Site': 'same-origin'}
        ))
        self.assertEqual(res.status_code, 204)

        res = self._run(client.post('/submit-exempt'))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.post(
            '/submit-exempt', headers={'Sec-Fetch-Site': 'cross-site'}
        ))
        self.assertEqual(res.status_code, 204)

    def test_allow_subdomains(self):
        app = Microdot()
        csrf = CSRF(allow_subdomains=True)
        csrf.initialize(app)

        @app.get('/')
        def index(request):
            return 204

        @app.post('/submit')
        def submit(request):
            return 204

        @app.post('/submit-exempt')
        @csrf.exempt
        def submit_exempt(request):
            return 204

        client = TestClient(app)

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.get(
            '/', headers={'Sec-Fetch-Site': 'cross-site'}
        ))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.get(
            '/', headers={'Origin': 'https://evil.com'}
        ))
        self.assertEqual(res.status_code, 204)

        res = self._run(client.post('/submit'))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.post(
            '/submit', headers={'Sec-Fetch-Site': 'cross-site'}
        ))
        self.assertEqual(res.status_code, 403)
        res = self._run(client.post(
            '/submit', headers={'Sec-Fetch-Site': 'same-site'}
        ))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.post(
            '/submit', headers={'Sec-Fetch-Site': 'same-origin'}
        ))
        self.assertEqual(res.status_code, 204)

        res = self._run(client.post('/submit-exempt'))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.post(
            '/submit-exempt', headers={'Sec-Fetch-Site': 'cross-site'}
        ))
        self.assertEqual(res.status_code, 204)

    def test_allowed_origins(self):
        app = Microdot()
        cors = CORS(allowed_origins=['http://foo.com', 'https://bar.com:8888'])
        csrf = CSRF()
        csrf.initialize(app, cors)

        @app.get('/')
        def index(request):
            return 204

        @app.post('/submit')
        def submit(request):
            return 204

        client = TestClient(app)

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.get(
            '/', headers={'Origin': 'foo.com'}
        ))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.get(
            '/', headers={'Origin': 'http://foo.com'}
        ))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.get(
            '/', headers={'Origin': 'https://baz.com'}
        ))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.get(
            '/', headers={'Origin': 'http://x.baz.com'}
        ))
        self.assertEqual(res.status_code, 204)

        res = self._run(client.post('/submit'))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.post(
            '/submit', headers={'Origin': 'https://bar.com:8888'}
        ))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.post(
            '/submit', headers={'Origin': 'http://bar.com:8888'}
        ))
        self.assertEqual(res.status_code, 403)
        res = self._run(client.post(
            '/submit', headers={'Origin': 'https://x.y.bar.com:8888'}
        ))
        self.assertEqual(res.status_code, 403)
        res = self._run(client.post(
            '/submit', headers={'Origin': 'http://baz.com'}
        ))
        self.assertEqual(res.status_code, 403)

    def test_allowed_origins_with_subdomains(self):
        app = Microdot()
        cors = CORS(allowed_origins=['http://foo.com', 'https://bar.com:8888'])
        csrf = CSRF(allow_subdomains=True)
        csrf.initialize(app, cors)

        @app.get('/')
        def index(request):
            return 204

        @app.post('/submit')
        def submit(request):
            return 204

        client = TestClient(app)

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.get(
            '/', headers={'Origin': 'foo.com'}
        ))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.get(
            '/', headers={'Origin': 'http://foo.com'}
        ))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.get(
            '/', headers={'Origin': 'https://baz.com'}
        ))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.get(
            '/', headers={'Origin': 'http://x.baz.com'}
        ))
        self.assertEqual(res.status_code, 204)

        res = self._run(client.post('/submit'))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.post(
            '/submit', headers={'Origin': 'https://bar.com:8888'}
        ))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.post(
            '/submit', headers={'Origin': 'https://x.y.bar.com:8888'}
        ))
        self.assertEqual(res.status_code, 204)
        res = self._run(client.post(
            '/submit', headers={'Origin': 'http://x.y.bar.com:8888'}
        ))
        self.assertEqual(res.status_code, 403)
        res = self._run(client.post(
            '/submit', headers={'Origin': 'http://baz.com'}
        ))
        self.assertEqual(res.status_code, 403)
