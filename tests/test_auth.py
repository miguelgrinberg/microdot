import asyncio
import binascii
import unittest
from microdot import Microdot
from microdot.auth import BasicAuth, TokenAuth
from microdot.test_client import TestClient


class TestAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if hasattr(asyncio, 'set_event_loop'):
            asyncio.set_event_loop(asyncio.new_event_loop())
        cls.loop = asyncio.get_event_loop()

    def _run(self, coro):
        return self.loop.run_until_complete(coro)

    def test_basic_auth(self):
        app = Microdot()
        basic_auth = BasicAuth()

        @basic_auth.authenticate
        def authenticate(request, username, password):
            if username == 'foo' and password == 'bar':
                return {'username': username}

        @app.route('/')
        @basic_auth
        def index(request):
            return request.g.current_user['username']

        client = TestClient(app)
        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 401)

        res = self._run(client.get('/', headers={
            'Authorization': 'Basic ' + binascii.b2a_base64(
                b'foo:bar').decode()}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'foo')

        res = self._run(client.get('/', headers={
            'Authorization': 'Basic ' + binascii.b2a_base64(
                b'foo:baz').decode()}))
        self.assertEqual(res.status_code, 401)

    def test_basic_optional_auth(self):
        app = Microdot()
        basic_auth = BasicAuth()

        @basic_auth.authenticate
        def authenticate(request, username, password):
            if username == 'foo' and password == 'bar':
                return {'username': username}

        @app.route('/')
        @basic_auth.optional
        def index(request):
            return request.g.current_user['username'] \
                if request.g.current_user else ''

        client = TestClient(app)
        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, '')

        res = self._run(client.get('/', headers={
            'Authorization': 'Basic ' + binascii.b2a_base64(
                b'foo:bar').decode()}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'foo')

        res = self._run(client.get('/', headers={
            'Authorization': 'Basic ' + binascii.b2a_base64(
                b'foo:baz').decode()}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, '')

    def test_token_auth(self):
        app = Microdot()
        token_auth = TokenAuth()

        @token_auth.authenticate
        def authenticate(request, token):
            if token == 'foo':
                return 'user'

        @app.route('/')
        @token_auth
        def index(request):
            return request.g.current_user

        client = TestClient(app)
        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 401)

        res = self._run(client.get('/', headers={
            'Authorization': 'Basic foo'}))
        self.assertEqual(res.status_code, 401)

        res = self._run(client.get('/', headers={'Authorization': 'invalid'}))
        self.assertEqual(res.status_code, 401)

        res = self._run(client.get('/', headers={
            'Authorization': 'Bearer foo'}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'user')

    def test_token_optional_auth(self):
        app = Microdot()
        token_auth = TokenAuth()

        @token_auth.authenticate
        def authenticate(request, token):
            if token == 'foo':
                return 'user'

        @app.route('/')
        @token_auth.optional
        def index(request):
            return request.g.current_user or ''

        client = TestClient(app)
        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, '')

        res = self._run(client.get('/', headers={
            'Authorization': 'Basic foo'}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, '')

        res = self._run(client.get('/', headers={'Authorization': 'foo'}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, '')

        res = self._run(client.get('/', headers={
            'Authorization': 'Bearer foo'}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'user')

    def test_token_auth_custom_header(self):
        app = Microdot()
        token_auth = TokenAuth(header='X-Auth-Token')

        @token_auth.authenticate
        def authenticate(request, token):
            if token == 'foo':
                return 'user'

        @app.route('/')
        @token_auth
        def index(request):
            return request.g.current_user

        client = TestClient(app)
        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 401)

        res = self._run(client.get('/', headers={
            'Authorization': 'Basic foo'}))
        self.assertEqual(res.status_code, 401)

        res = self._run(client.get('/', headers={'Authorization': 'foo'}))
        self.assertEqual(res.status_code, 401)

        res = self._run(client.get('/', headers={
            'Authorization': 'Bearer foo'}))
        self.assertEqual(res.status_code, 401)

        res = self._run(client.get('/', headers={
            'X-Token-Auth': 'Bearer foo'}))
        self.assertEqual(res.status_code, 401)

        res = self._run(client.get('/', headers={'X-Auth-Token': 'foo'}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'user')

        res = self._run(client.get('/', headers={'x-auth-token': 'foo'}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'user')

        @token_auth.errorhandler
        def error_handler(request):
            return {'status_code': 403}, 403

        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json, {'status_code': 403})
