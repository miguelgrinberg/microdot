import unittest
from microdot import Microdot
from microdot_session import set_session_secret_key, get_session, \
    update_session, delete_session, with_session
from microdot_test_client import TestClient

set_session_secret_key('top-secret!')


class TestSession(unittest.TestCase):
    def setUp(self):
        self.app = Microdot()
        self.client = TestClient(self.app)

    def tearDown(self):
        pass

    def test_session(self):
        @self.app.get('/')
        def index(req):
            session = get_session(req)
            return str(session.get('name'))

        @self.app.get('/with')
        @with_session
        def session_context_manager(req, session):
            return str(session.get('name'))

        @self.app.post('/set')
        def set_session(req):
            update_session(req, {'name': 'joe'})
            return 'OK'

        @self.app.post('/del')
        def del_session(req):
            delete_session(req)
            return 'OK'

        res = self.client.get('/')
        self.assertEqual(res.text, 'None')
        res = self.client.get('/with')
        self.assertEqual(res.text, 'None')

        res = self.client.post('/set')
        self.assertEqual(res.text, 'OK')

        res = self.client.get('/')
        self.assertEqual(res.text, 'joe')
        res = self.client.get('/with')
        self.assertEqual(res.text, 'joe')

        res = self.client.post('/del')
        self.assertEqual(res.text, 'OK')

        res = self.client.get('/')
        self.assertEqual(res.text, 'None')
        res = self.client.get('/with')
        self.assertEqual(res.text, 'None')

    def test_session_no_secret_key(self):
        set_session_secret_key(None)

        @self.app.get('/')
        def index(req):
            self.assertRaises(ValueError, get_session, req)
            self.assertRaises(ValueError, update_session, req, {})
            return ''

        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

        set_session_secret_key('top-secret!')
