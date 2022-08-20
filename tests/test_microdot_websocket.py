import unittest
from microdot import Microdot
from microdot_websocket import with_websocket
from microdot_test_client import TestClient
from tests import mock_socket


class TestMicrodotWebSocket(unittest.TestCase):
    def test_websocket_echo(self):
        app = Microdot()

        @app.route('/echo')
        @with_websocket
        def index(req, ws):
            while True:
                data = ws.receive()
                ws.send(data)

        def ws():
            data = yield 'hello'
            self.assertEqual(data, 'hello')
            data = yield b'bye'
            self.assertEqual(data, b'bye')

        client = TestClient(app)
        res = client.websocket('/echo', ws)
        self.assertIsNone(res)
