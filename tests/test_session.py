try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
import unittest
from microdot import Microdot
from microdot_asyncio import Microdot as MicrodotAsync
from microdot_session import set_session_secret_key, get_session, \
    update_session, delete_session, with_session
from microdot_test_client import TestClient
from microdot_asyncio_test_client import TestClient as TestClientAsync

set_session_secret_key('top-secret!')


class TestSession(unittest.TestCase):
    def test_session(self):
        app = Microdot()
        client = TestClient(app)

        @app.get('/')
        def index(req):
            session = get_session(req)
            session2 = get_session(req)
            session2['foo'] = 'bar'
            self.assertEqual(session['foo'], 'bar')
            return str(session.get('name'))

        @app.get('/with')
        @with_session
        def session_context_manager(req, session):
            return str(session.get('name'))

        @app.post('/set')
        def set_session(req):
            update_session(req, {'name': 'joe'})
            return 'OK'

        @app.post('/del')
        def del_session(req):
            delete_session(req)
            return 'OK'

        res = client.get('/')
        self.assertEqual(res.text, 'None')
        res = client.get('/with')
        self.assertEqual(res.text, 'None')

        res = client.post('/set')
        self.assertEqual(res.text, 'OK')

        res = client.get('/')
        self.assertEqual(res.text, 'joe')
        res = client.get('/with')
        self.assertEqual(res.text, 'joe')

        res = client.post('/del')
        self.assertEqual(res.text, 'OK')

        res = client.get('/')
        self.assertEqual(res.text, 'None')
        res = client.get('/with')
        self.assertEqual(res.text, 'None')

    def _run(self, coro):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro)

    def test_session_async(self):
        app = MicrodotAsync()
        client = TestClientAsync(app)

        @app.get('/')
        async def index(req):
            session = get_session(req)
            session2 = get_session(req)
            session2['foo'] = 'bar'
            self.assertEqual(session['foo'], 'bar')
            return str(session.get('name'))

        @app.get('/with')
        @with_session
        async def session_context_manager(req, session):
            return str(session.get('name'))

        @app.post('/set')
        async def set_session(req):
            update_session(req, {'name': 'joe'})
            return 'OK'

        @app.post('/del')
        async def del_session(req):
            delete_session(req)
            return 'OK'

        res = self._run(client.get('/'))
        self.assertEqual(res.text, 'None')
        res = self._run(client.get('/with'))
        self.assertEqual(res.text, 'None')

        res = self._run(client.post('/set'))
        self.assertEqual(res.text, 'OK')

        res = self._run(client.get('/'))
        self.assertEqual(res.text, 'joe')
        res = self._run(client.get('/with'))
        self.assertEqual(res.text, 'joe')

        res = self._run(client.post('/del'))
        self.assertEqual(res.text, 'OK')

        res = self._run(client.get('/'))
        self.assertEqual(res.text, 'None')
        res = self._run(client.get('/with'))
        self.assertEqual(res.text, 'None')

    def test_session_no_secret_key(self):
        set_session_secret_key(None)
        app = Microdot()
        client = TestClient(app)

        @app.get('/')
        def index(req):
            self.assertRaises(ValueError, get_session, req)
            self.assertRaises(ValueError, update_session, req, {})
            return ''

        res = client.get('/')
        self.assertEqual(res.status_code, 200)

        set_session_secret_key('top-secret!')
