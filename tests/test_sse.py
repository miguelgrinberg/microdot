import asyncio
import unittest
from microdot import Microdot
from microdot.sse import with_sse
from microdot.test_client import TestClient


class TestWebSocket(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if hasattr(asyncio, 'set_event_loop'):
            asyncio.set_event_loop(asyncio.new_event_loop())
        cls.loop = asyncio.get_event_loop()

    def _run(self, coro):
        return self.loop.run_until_complete(coro)

    def test_sse(self):
        app = Microdot()

        @app.route('/sse')
        @with_sse
        async def handle_sse(request, sse):
            await sse.send('foo')
            await sse.send('bar', event='test')
            await sse.send({'foo': 'bar'})
            await sse.send([42, 'foo', 'bar'])
            await sse.send(ValueError('foo'))

        client = TestClient(app)
        response = self._run(client.get('/sse'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/event-stream')
        self.assertEqual(response.text, ('data: foo\n\n'
                                         'event: test\ndata: bar\n\n'
                                         'data: {"foo": "bar"}\n\n'
                                         'data: [42, "foo", "bar"]\n\n'
                                         'data: foo\n\n'))
