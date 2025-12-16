import asyncio
import unittest
from microdot import Microdot
from microdot.csrf import CSRF
from microdot.login import Login
from microdot.session import Session
from microdot.test_client import TestClient
try:
    from unittest import mock
except ImportError:
    from tests import mock


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
        Session(app, 'top-secret')
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

        client = TestClient(app)

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 204)
        csrf_token = client.cookies['_csrf_token']

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
        Session(app, 'top-secret')
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
        csrf_token = client.cookies['_csrf_token']

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
        Session(app, 'top-secret')
        csrf = CSRF(secret_key='top-secret', time_limit=600,
                    cookie_options={'path': '/'})
        csrf.initialize(app)
        self.assertEqual(csrf.secret_key, b'top-secret')
        self.assertEqual(csrf.time_limit, 600)
        self.assertEqual(csrf.cookie_options, {'path': '/'})
        self.assertEqual(csrf.protect_all, True)

    def test_initialize_with_overrides(self):
        app = Microdot()
        Session(app, 'top-secret')
        csrf = CSRF(secret_key='top-secret', time_limit=600,
                    cookie_options={'path': '/'})
        csrf.initialize(app, secret_key=b'another-key', time_limit=1200,
                        cookie_options={}, protect_all=False)
        self.assertEqual(csrf.secret_key, b'another-key')
        self.assertEqual(csrf.time_limit, 1200)
        self.assertEqual(csrf.cookie_options, {})
        self.assertEqual(csrf.protect_all, False)

    def test_logged_in_user(self):
        app = Microdot()
        Session(app, 'top-secret')
        login = Login()
        csrf = CSRF()
        csrf.initialize(app)
        mocked_gen = mock.patch(
            'microdot.csrf.CSRF.generate_csrf_token_payload',
            return_value=b'1234.5678')
        mocked_gen.start()

        @login.user_loader
        def load_user(user_id):
            return User(user_id)

        class User:
            def __init__(self, id):
                self.id = id

        @app.get('/user1')
        async def index(request):
            await login.login_user(request, User(1234))
            return 204

        @app.get('/user2')
        async def index2(request):
            await login.login_user(request, User(4321))
            return 204

        @app.post('/submit')
        @login
        def submit(request):
            return 204

        client = TestClient(app)

        res = self._run(client.get('/user1'))
        self.assertEqual(res.status_code, 204)
        csrf_token = client.cookies['_csrf_token']

        res = self._run(client.post('/submit',
                                    headers={'X-CSRF-Token': csrf_token}))
        self.assertEqual(res.status_code, 204)

        res = self._run(client.get('/user2'))
        self.assertEqual(res.status_code, 204)
        csrf_token2 = client.cookies['_csrf_token']
        assert csrf_token != csrf_token2

        res = self._run(client.post('/submit',
                                    headers={'X-CSRF-Token': csrf_token}))
        self.assertEqual(res.status_code, 403)
        res = self._run(client.post('/submit',
                                    headers={'X-CSRF-Token': csrf_token2}))
        self.assertEqual(res.status_code, 204)

        mocked_gen.stop()

    def test_token_expired(self):
        app = Microdot()
        Session(app, b'top-secret')
        CSRF(app, time_limit=60)

        @app.get('/')
        def index(request):
            return 204

        @app.post('/submit')
        def submit(request):
            return 204

        client = TestClient(app)

        with mock.patch('microdot.csrf.time', return_value=1000):
            res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 204)
        csrf_token = client.cookies['_csrf_token']

        with mock.patch('microdot.csrf.time', return_value=1020):
            res = self._run(client.post(
                '/submit',
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                body='csrf_token=' + csrf_token,
            ))
        self.assertEqual(res.status_code, 204)

        with mock.patch('microdot.csrf.time', return_value=1100):
            res = self._run(client.post(
                '/submit',
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                body='csrf_token=' + csrf_token,
            ))
        self.assertEqual(res.status_code, 403)

    def test_cookie_is_secure(self):
        app = Microdot()
        CSRF(app, 'top-secret', time_limit=60)

        @app.get('/')
        def index(request):
            return 204

        @app.post('/submit')
        def submit(request):
            return 204

        client = TestClient(app, scheme='https')

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 204)
        self.assertIn('; Secure', res.headers['Set-Cookie'][0])
