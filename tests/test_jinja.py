import asyncio
import sys
import unittest
from microdot import Microdot
from microdot.jinja import Template
from microdot.test_client import TestClient

Template.initialize('tests/templates')


@unittest.skipIf(sys.implementation.name == 'micropython',
                 'not supported under MicroPython')
class TestJinja(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if hasattr(asyncio, 'set_event_loop'):
            asyncio.set_event_loop(asyncio.new_event_loop())
        cls.loop = asyncio.get_event_loop()

    def _run(self, coro):
        return self.loop.run_until_complete(coro)

    def test_render_template(self):
        s = Template('hello.jinja.txt').render(name='foo')
        self.assertEqual(s, 'Hello, foo!')

    def test_render_template_in_app(self):
        app = Microdot()

        @app.route('/')
        async def index(req):
            return Template('hello.jinja.txt').render(name='foo')

        client = TestClient(app)
        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.body, b'Hello, foo!')

    def test_generate_template_in_app(self):
        app = Microdot()

        @app.route('/')
        async def index(req):
            return Template('hello.jinja.txt').generate(name='foo')

        client = TestClient(app)
        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.body, b'Hello, foo!')

    def test_render_async_template_in_app(self):
        Template.initialize('tests/templates', enable_async=True)

        app = Microdot()

        @app.route('/')
        async def index(req):
            return await Template('hello.jinja.txt').render_async(name='foo')

        client = TestClient(app)
        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.body, b'Hello, foo!')

        Template.initialize('tests/templates')

    def test_generate_async_template_in_app(self):
        Template.initialize('tests/templates', enable_async=True)

        app = Microdot()

        @app.route('/')
        async def index(req):
            return Template('hello.jinja.txt').generate_async(name='foo')

        client = TestClient(app)
        res = self._run(client.get('/'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.body, b'Hello, foo!')

        Template.initialize('tests/templates')
