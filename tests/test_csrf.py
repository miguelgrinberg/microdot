import asyncio
import time
import unittest
from microdot import Microdot
from microdot.csrf import CSRF
from microdot.test_client import TestClient


class TestMicrodot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if hasattr(asyncio, 'set_event_loop'):
            asyncio.set_event_loop(asyncio.new_event_loop())
        cls.loop = asyncio.get_event_loop()

    def _run(self, coro):
        return self.loop.run_until_complete(coro)

    def test_protect_all_true(self):
        app = Microdot()
        csrf = CSRF(app, 'top-secret')

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
        csrf_token = client.cookies['csrf_token']

        res = self._run(client.post('/submit'))
        self.assertEqual(res.status_code, 403)

        res = self._run(client.post(
            '/submit',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            body='csrf_token=' + csrf_token,
        ))
        self.assertEqual(res.status_code, 204)

        res = self._run(client.post(
            '/submit',
            headers={'X-CSRF-Token': csrf_token},
        ))
        self.assertEqual(res.status_code, 204)

        res = self._run(client.post('/submit-exempt'))
        self.assertEqual(res.status_code, 204)

    def test_protect_all_false(self):
        app = Microdot()
        csrf = CSRF()
        csrf.initialize(app, b'top-secret', protect_all=False)

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
        csrf_token = client.cookies['csrf_token']

        res = self._run(client.post('/submit'))
        self.assertEqual(res.status_code, 403)

        res = self._run(client.post(
            '/submit',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            body='csrf_token=' + csrf_token,
        ))
        self.assertEqual(res.status_code, 204)

        res = self._run(client.post(
            '/submit',
            headers={'X-CSRF-Token': csrf_token},
        ))
        self.assertEqual(res.status_code, 204)

        res = self._run(client.post('/submit-exempt'))
        self.assertEqual(res.status_code, 204)

    def test_initialize_with_defaults(self):
        app = Microdot()
        csrf = CSRF(secret_key='top-secret', time_limit=600,
                    cookie_options={'path': '/'})
        csrf.initialize(app)
        self.assertEqual(csrf.secret_key, b'top-secret')
        self.assertEqual(csrf.time_limit, 600)
        self.assertEqual(csrf.cookie_options, {'path': '/'})
        self.assertEqual(csrf.protect_all, True)

    def test_initialize_with_overrides(self):
        app = Microdot()
        csrf = CSRF(secret_key='top-secret', time_limit=600,
                    cookie_options={'path': '/'})
        csrf.initialize(app, secret_key=b'another-key', time_limit=1200,
                        cookie_options={}, protect_all=False)
        self.assertEqual(csrf.secret_key, b'another-key')
        self.assertEqual(csrf.time_limit, 1200)
        self.assertEqual(csrf.cookie_options, {})
        self.assertEqual(csrf.protect_all, False)

    def test_token_expired(self):
        app = Microdot()
        CSRF(app, 'top-secret', time_limit=0.25)

        @app.get('/')
        def index(request):
            return 204

        @app.post('/submit')
        def submit(request):
            return 204

        client = TestClient(app)

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 204)
        csrf_token = client.cookies['csrf_token']

        res = self._run(client.post(
            '/submit',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            body='csrf_token=' + csrf_token,
        ))
        self.assertEqual(res.status_code, 204)

        time.sleep(0.25)
        res = self._run(client.post(
            '/submit',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            body='csrf_token=' + csrf_token,
        ))
        self.assertEqual(res.status_code, 403)

    def test_cookie_is_secure(self):
        app = Microdot()
        CSRF(app, 'top-secret', time_limit=0.25)

        @app.get('/')
        def index(request):
            print(request.url)
            return 204

        @app.post('/submit')
        def submit(request):
            return 204

        client = TestClient(app, scheme='https')

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 204)
        self.assertIn('; Secure', res.headers['Set-Cookie'][0])
