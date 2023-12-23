import asyncio
import unittest
from microdot import Microdot
from microdot.test_client import TestClient
from microdot.utemplate import Template

Template.initialize('tests/templates')


class TestUTemplate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if hasattr(asyncio, 'set_event_loop'):
            asyncio.set_event_loop(asyncio.new_event_loop())
        cls.loop = asyncio.get_event_loop()

    def _run(self, coro):
        return self.loop.run_until_complete(coro)

    def test_render_template(self):
        s = Template('hello.utemplate.txt').render(name='foo')
        self.assertEqual(s, 'Hello, foo!\n')

    def test_render_template_in_app(self):
        app = Microdot()

        @app.route('/')
        async def index(req):
            return Template('hello.utemplate.txt').render(name='foo')

        client = TestClient(app)
        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.body, b'Hello, foo!\n')

    def test_render_async_template_in_app(self):
        app = Microdot()

        @app.route('/')
        async def index(req):
            return await Template('hello.utemplate.txt').render_async(
                name='foo')

        client = TestClient(app)
        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.body, b'Hello, foo!\n')
