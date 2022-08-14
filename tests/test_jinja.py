try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

import sys
import unittest
from microdot import Microdot, Request
from microdot_asyncio import Microdot as MicrodotAsync, Request as RequestAsync
from microdot_jinja import render_template, init_templates
from tests.mock_socket import get_request_fd, get_async_request_fd

init_templates('tests/templates')


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


@unittest.skipIf(sys.implementation.name == 'micropython',
                 'not supported under MicroPython')
class TestJinja(unittest.TestCase):
    def test_render_template(self):
        s = render_template('hello.jinja.txt', name='foo')
        self.assertEqual(s, 'Hello, foo!')

    def test_render_template_in_app(self):
        app = Microdot()

        @app.route('/')
        def index(req):
            return render_template('hello.jinja.txt', name='foo')

        req = Request.create(app, get_request_fd('GET', '/'), 'addr')
        res = app.dispatch_request(req)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.body_iter()), [b'Hello, foo!'])

    def test_render_template_in_app_async(self):
        app = MicrodotAsync()

        @app.route('/')
        async def index(req):
            return render_template('hello.jinja.txt', name='foo')

        req = _run(RequestAsync.create(
            app, get_async_request_fd('GET', '/'), 'writer', 'addr'))
        res = _run(app.dispatch_request(req))
        self.assertEqual(res.status_code, 200)

        async def get_result():
            result = []
            async for chunk in res.body_iter():
                result.append(chunk)
            return result

        result = _run(get_result())
        self.assertEqual(result, [b'Hello, foo!'])
