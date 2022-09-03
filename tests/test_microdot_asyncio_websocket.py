import sys
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
import unittest
from microdot_asyncio import Microdot
from microdot_asyncio_websocket import with_websocket
from microdot_asyncio_test_client import TestClient


class TestMicrodotAsyncWebSocket(unittest.TestCase):
    def _run(self, coro):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro)

    def test_websocket_echo(self):
        app = Microdot()

        @app.route('/echo')
        @with_websocket
        async def index(req, ws):
            while True:
                data = await ws.receive()
                await ws.send(data)

        results = []

        def ws():
            data = yield 'hello'
            results.append(data)
            data = yield b'bye'
            results.append(data)
            data = yield b'*' * 300
            results.append(data)
            data = yield b'+' * 65537
            results.append(data)

        client = TestClient(app)
        res = self._run(client.websocket('/echo', ws))
        self.assertIsNone(res)
        self.assertEqual(results, ['hello', b'bye', b'*' * 300, b'+' * 65537])

    @unittest.skipIf(sys.implementation.name == 'micropython',
                     'no support for async generators in MicroPython')
    def test_websocket_echo_async_client(self):
        app = Microdot()

        @app.route('/echo')
        @with_websocket
        async def index(req, ws):
            while True:
                data = await ws.receive()
                await ws.send(data)

        results = []

        async def ws():
            data = yield 'hello'
            results.append(data)
            data = yield b'bye'
            results.append(data)
            data = yield b'*' * 300
            results.append(data)
            data = yield b'+' * 65537
            results.append(data)

        client = TestClient(app)
        res = self._run(client.websocket('/echo', ws))
        self.assertIsNone(res)
        self.assertEqual(results, ['hello', b'bye', b'*' * 300, b'+' * 65537])
