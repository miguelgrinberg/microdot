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
            await sse.send('bar', event='test', event_id='id42')
            await sse.send('bar', event_id='id42')
            await sse.send({'foo': 'bar'})
            await sse.send([42, 'foo', 'bar'])
            await sse.send(ValueError('foo'))
            await sse.send(b'foo')

        client = TestClient(app)
        response = self._run(client.get('/sse'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/event-stream')
        self.assertEqual(response.text, ('data: foo\n\n'
                                         'event: test\ndata: bar\n\n'
                                         'event: test\nid: id42\ndata: bar\n\n'
                                         'id: id42\ndata: bar\n\n'
                                         'data: {"foo": "bar"}\n\n'
                                         'data: [42, "foo", "bar"]\n\n'
                                         'data: foo\n\n'
                                         'data: foo\n\n'))
        self.assertEqual(len(response.events), 8)
        self.assertEqual(response.events[0], {
            'data': b'foo', 'data_json': None, 'event': None,
            'event_id': None})
        self.assertEqual(response.events[1], {
            'data': b'bar', 'data_json': None, 'event': 'test',
            'event_id': None})
        self.assertEqual(response.events[2], {
            'data': b'bar', 'data_json': None, 'event': 'test',
            'event_id': 'id42'})
        self.assertEqual(response.events[3], {
            'data': b'bar', 'data_json': None, 'event': None,
            'event_id': 'id42'})
        self.assertEqual(response.events[4], {
            'data': b'{"foo": "bar"}', 'data_json': {'foo': 'bar'},
            'event': None, 'event_id': None})
        self.assertEqual(response.events[5], {
            'data': b'[42, "foo", "bar"]', 'data_json': [42, 'foo', 'bar'],
            'event': None, 'event_id': None})
        self.assertEqual(response.events[6], {
            'data': b'foo', 'data_json': None, 'event': None,
            'event_id': None})
        self.assertEqual(response.events[7], {
            'data': b'foo', 'data_json': None, 'event': None,
            'event_id': None})

    def test_sse_exception(self):
        app = Microdot()

        @app.route('/sse')
        @with_sse
        async def handle_sse(request, sse):
            await sse.send('foo')
            await sse.send(1 / 0)

        client = TestClient(app)
        self.assertRaises(ZeroDivisionError, self._run, client.get('/sse'))
