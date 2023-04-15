try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
import unittest
from microdot import Microdot
from microdot.asyncio import Microdot as MicrodotAsync
from microdot.session import Session, with_session
from microdot.test_client import TestClient
from microdot.asyncio.test_client import TestClient as TestClientAsync

session_ext = Session(secret_key='top-secret!')


class TestSession(unittest.TestCase):
    def test_session(self):
        app = Microdot()
        session_ext.initialize(app)
        client = TestClient(app)

        @app.get('/')
        def index(req):
            session = session_ext.get(req)
            session2 = session_ext.get(req)
            session2['foo'] = 'bar'
            self.assertEqual(session['foo'], 'bar')
            return str(session.get('name'))

        @app.get('/with')
        @with_session
        def session_context_manager(req, session):
            return str(session.get('name'))

        @app.post('/set')
        @with_session
        def save_session(req, session):
            session['name'] = 'joe'
            session.save()
            return 'OK'

        @app.post('/del')
        @with_session
        def delete_session(req, session):
            session.delete()
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
        session_ext.initialize(app, secret_key='some-other-secret')
        client = TestClientAsync(app)

        @app.get('/')
        async def index(req):
            session = session_ext.get(req)
            session2 = session_ext.get(req)
            session2['foo'] = 'bar'
            self.assertEqual(session['foo'], 'bar')
            return str(session.get('name'))

        @app.get('/with')
        @with_session
        async def session_context_manager(req, session):
            return str(session.get('name'))

        @app.post('/set')
        @with_session
        async def save_session(req, session):
            session['name'] = 'joe'
            session.save()
            return 'OK'

        @app.post('/del')
        @with_session
        async def delete_session(req, session):
            session.delete()
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
        app = Microdot()
        session_ext = Session(app)
        client = TestClient(app)

        @app.get('/')
        def index(req):
            self.assertRaises(ValueError, session_ext.get, req)
            self.assertRaises(ValueError, session_ext.update, req, {})
            return ''

        res = client.get('/')
        self.assertEqual(res.status_code, 200)
