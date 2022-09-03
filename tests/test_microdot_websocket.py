import unittest
from microdot import Microdot
from microdot_websocket import with_websocket, WebSocket
from microdot_test_client import TestClient


class TestMicrodotWebSocket(unittest.TestCase):
    def test_websocket_echo(self):
        app = Microdot()

        @app.route('/echo')
        @with_websocket
        def index(req, ws):
            while True:
                data = ws.receive()
                ws.send(data)

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
        res = client.websocket('/echo', ws)
        self.assertIsNone(res)
        self.assertEqual(results, ['hello', b'bye', b'*' * 300, b'+' * 65537])

    def test_bad_websocket_request(self):
        app = Microdot()

        @app.route('/echo')
        @with_websocket
        def index(req, ws):
            return 'hello'

        client = TestClient(app)
        res = client.get('/echo')
        self.assertEqual(res.status_code, 400)
        res = client.get('/echo', headers={'Connection': 'Upgrade'})
        self.assertEqual(res.status_code, 400)
        res = client.get('/echo', headers={'Connection': 'foo'})
        self.assertEqual(res.status_code, 400)
        res = client.get('/echo', headers={'Upgrade': 'websocket'})
        self.assertEqual(res.status_code, 400)
        res = client.get('/echo', headers={'Upgrade': 'bar'})
        self.assertEqual(res.status_code, 400)
        res = client.get('/echo', headers={'Connection': 'Upgrade',
                                           'Upgrade': 'websocket'})
        self.assertEqual(res.status_code, 400)
        res = client.get('/echo', headers={'Sec-WebSocket-Key': 'xxx'})
        self.assertEqual(res.status_code, 400)

    def test_process_websocket_frame(self):
        ws = WebSocket(None)
        ws.closed = True

        self.assertEqual(ws._process_websocket_frame(WebSocket.TEXT, b'foo'),
                         (None, 'foo'))
        self.assertEqual(ws._process_websocket_frame(WebSocket.BINARY, b'foo'),
                         (None, b'foo'))
        self.assertRaises(OSError, ws._process_websocket_frame,
                          WebSocket.CLOSE, b'')
        self.assertEqual(ws._process_websocket_frame(WebSocket.PING, b'foo'),
                         (WebSocket.PONG, b'foo'))
        self.assertEqual(ws._process_websocket_frame(WebSocket.PONG, b'foo'),
                         (None, None))
