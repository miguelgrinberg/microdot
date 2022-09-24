import binascii
import unittest
from microdot import Microdot
from microdot_auth import BasicAuth, TokenAuth
from microdot_test_client import TestClient


class TestAuth(unittest.TestCase):
    def test_basic_auth(self):
        app = Microdot()
        basic_auth = BasicAuth()

        @basic_auth.callback
        def authenticate(request, username, password):
            if username == 'foo' and password == 'bar':
                request.g.user = {'username': username}
                return True

        @app.route('/')
        @basic_auth
        def index(request):
            return request.g.user['username']

        client = TestClient(app)
        res = client.get('/')
        self.assertEqual(res.status_code, 401)

        res = client.get('/', headers={
            'Authorization': 'Basic ' + binascii.b2a_base64(
                b'foo:bar').decode()})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'foo')

        res = client.get('/', headers={
            'Authorization': 'Basic ' + binascii.b2a_base64(
                b'foo:baz').decode()})
        self.assertEqual(res.status_code, 401)

    def test_token_auth(self):
        app = Microdot()
        token_auth = TokenAuth()

        @token_auth.callback
        def authenticate(request, token):
            if token == 'foo':
                request.g.user = 'user'
                return True

        @app.route('/')
        @token_auth
        def index(request):
            return request.g.user

        client = TestClient(app)
        res = client.get('/')
        self.assertEqual(res.status_code, 401)

        res = client.get('/', headers={'Authorization': 'Basic foo'})
        self.assertEqual(res.status_code, 401)

        res = client.get('/', headers={'Authorization': 'foo'})
        self.assertEqual(res.status_code, 401)

        res = client.get('/', headers={'Authorization': 'Bearer foo'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'user')

    def test_token_auth_custom_header(self):
        app = Microdot()
        token_auth = TokenAuth(header='X-Auth-Token')

        @token_auth.callback
        def authenticate(request, token):
            if token == 'foo':
                request.g.user = 'user'
                return True

        @app.route('/')
        @token_auth
        def index(request):
            return request.g.user

        client = TestClient(app)
        res = client.get('/')
        self.assertEqual(res.status_code, 401)

        res = client.get('/', headers={'Authorization': 'Basic foo'})
        self.assertEqual(res.status_code, 401)

        res = client.get('/', headers={'Authorization': 'foo'})
        self.assertEqual(res.status_code, 401)

        res = client.get('/', headers={'Authorization': 'Bearer foo'})
        self.assertEqual(res.status_code, 401)

        res = client.get('/', headers={'X-Token-Auth': 'Bearer foo'})
        self.assertEqual(res.status_code, 401)

        res = client.get('/', headers={'X-Auth-Token': 'foo'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'user')

        res = client.get('/', headers={'x-auth-token': 'foo'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'user')

        @token_auth.errorhandler
        def error_handler():
            return {'status_code': 403}, 403

        res = client.get('/')
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json, {'status_code': 403})
