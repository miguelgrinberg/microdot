import asyncio
import unittest
from microdot import Microdot
from microdot.login import Login
from microdot.session import Session
from microdot.test_client import TestClient


class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if hasattr(asyncio, 'set_event_loop'):
            asyncio.set_event_loop(asyncio.new_event_loop())
        cls.loop = asyncio.get_event_loop()

    def _run(self, coro):
        return self.loop.run_until_complete(coro)

    def test_login(self):
        app = Microdot()
        Session(app, secret_key='secret')
        login = Login()

        class User:
            def __init__(self, id, name):
                self.id = id
                self.name = name

        @login.id_to_user
        def id_to_user(user_id):
            return User(user_id, f'user{user_id}')

        @app.get('/')
        @login
        def index(request):
            return request.g.current_user.name

        @app.post('/login')
        async def login_route(request):
            return await login.login_user(request, User(123, 'user123'))

        @app.post('/logout')
        async def logout_route(request):
            await login.logout_user(request)
            return 'ok'

        client = TestClient(app)
        res = self._run(client.get('/?foo=bar'))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers['Location'], '/login?next=/%3Ffoo%3Dbar')

        res = self._run(client.post('/login?next=/%3Ffoo=bar'))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers['Location'], '/?foo=bar')
        self.assertEqual(len(res.headers['Set-Cookie']), 1)
        self.assertIn('session', client.cookies)

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'user123')

        res = self._run(client.post('/logout'))
        self.assertEqual(res.status_code, 200)

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 302)

    def test_login_bad_user_id(self):
        app = Microdot()
        Session(app, secret_key='secret')
        login = Login()

        @login.id_to_user
        def id_to_user(user_id):
            return None

        @login.user_to_id
        def user_to_id(user):
            return user

        @app.get('/foo')
        @login
        async def index(request):
            return 'ok'

        @app.post('/login')
        async def login_route(request):
            return await login.login_user(request, 'user')

        client = TestClient(app)
        res = self._run(client.post('/login?next=/'))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers['Location'], '/')
        res = self._run(client.get('/foo'))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers['Location'], '/login?next=/foo')

    def test_login_bad_redirect(self):
        app = Microdot()
        Session(app, secret_key='secret')
        login = Login()

        @login.id_to_user
        def id_to_user(user_id):
            return user_id

        @login.user_to_id
        def user_to_id(user):
            return user

        @app.get('/')
        @login
        async def index(request):
            return 'ok'

        @app.post('/login')
        async def login_route(request):
            return await login.login_user(request, 'user')

        client = TestClient(app)
        res = self._run(client.post('/login?next=http://example.com'))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers['Location'], '/')

    def test_login_remember(self):
        app = Microdot()
        Session(app, secret_key='secret')
        login = Login()

        @login.id_to_user
        def id_to_user(user_id):
            return user_id

        @login.user_to_id
        def user_to_id(user):
            return user

        @app.get('/')
        @login
        def index(request):
            return request.g.current_user

        @app.post('/login')
        async def login_route(request):
            return await login.login_user(request, 'user', remember=True)

        @app.post('/logout')
        async def logout(request):
            await login.logout_user(request)
            return 'ok'

        @app.get('/fresh')
        @login.fresh
        async def fresh(request):
            return f'fresh {request.g.current_user}'

        client = TestClient(app)
        res = self._run(client.post('/login?next=/%3Ffoo=bar'))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers['Location'], '/?foo=bar')
        self.assertEqual(len(res.headers['Set-Cookie']), 2)
        self.assertIn('session', client.cookies)
        self.assertIn('_remember', client.cookies)

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'user')
        res = self._run(client.get('/fresh'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'fresh user')

        del client.cookies['session']
        print(client.cookies)
        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        res = self._run(client.get('/fresh'))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers['Location'], '/login?next=/fresh')

        res = self._run(client.post('/logout'))
        self.assertEqual(res.status_code, 200)
        self.assertFalse('_remember' in client.cookies)

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 302)
