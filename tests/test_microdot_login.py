import unittest
from microdot import Microdot
from microdot_login import LoginAuth
from microdot_session import set_session_secret_key, with_session
from microdot_test_client import TestClient

set_session_secret_key('top-secret!')


class TestLogin(unittest.TestCase):
    def test_login_auth(self):
        app = Microdot()
        login_auth = LoginAuth()

        @app.get('/')
        @login_auth
        def index(request):
            return 'ok'

        @app.post('/login')
        def login(request):
            login_auth.login_user(request, 'user')
            return login_auth.redirect_to_next(request)

        @app.post('/logout')
        def logout(request):
            login_auth.logout_user(request)
            return 'ok'

        client = TestClient(app)
        res = client.get('/?foo=bar')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers['Location'], '/login?next=/%3Ffoo%3Dbar')

        res = client.post('/login?next=/%3Ffoo=bar')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers['Location'], '/?foo=bar')

        res = client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'ok')

        res = client.post('/logout')
        self.assertEqual(res.status_code, 200)

        res = client.get('/')
        self.assertEqual(res.status_code, 302)

    def test_login_auth_with_session(self):
        app = Microdot()
        login_auth = LoginAuth(login_url='/foo')

        @app.get('/')
        @login_auth
        @with_session
        def index(request, session):
            return session['user_id']

        @app.post('/foo')
        def login(request):
            login_auth.login_user(request, 'user')
            return login_auth.redirect_to_next(request)

        client = TestClient(app)
        res = client.get('/')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers['Location'], '/foo?next=/')

        res = client.post('/foo')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers['Location'], '/')

        res = client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'user')

    def test_login_auth_user_callback(self):
        app = Microdot()
        login_auth = LoginAuth()

        @login_auth.callback
        def check_user(request, user_id):
            request.g.user_id = user_id
            return user_id == 'user'

        @app.get('/')
        @login_auth
        def index(request):
            return request.g.user_id

        @app.post('/good-login')
        def good_login(request):
            login_auth.login_user(request, 'user')
            return login_auth.redirect_to_next(request)

        @app.post('/bad-login')
        def bad_login(request):
            login_auth.login_user(request, 'foo')
            return login_auth.redirect_to_next(request)

        client = TestClient(app)
        res = client.post('/good-login')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers['Location'], '/')
        res = client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'user')

        res = client.post('/bad-login')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers['Location'], '/')
        res = client.get('/')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers['Location'], '/login?next=/')

    def test_login_auth_bad_redirect(self):
        app = Microdot()
        login_auth = LoginAuth()

        @app.get('/')
        @login_auth
        def index(request):
            return 'ok'

        @app.post('/login')
        def login(request):
            login_auth.login_user(request, 'user')
            return login_auth.redirect_to_next(request)

        client = TestClient(app)
        res = client.post('/login?next=http://example.com')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers['Location'], '/')

