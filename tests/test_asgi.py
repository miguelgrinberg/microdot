import asyncio
import sys
import unittest
from unittest import mock

from microdot.asgi import Microdot, Response


@unittest.skipIf(sys.implementation.name == 'micropython',
                 'not supported under MicroPython')
class TestASGI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if hasattr(asyncio, 'set_event_loop'):
            asyncio.set_event_loop(asyncio.new_event_loop())
        cls.loop = asyncio.get_event_loop()

    def _run(self, coro):
        return self.loop.run_until_complete(coro)

    def test_asgi_request_with_query_string(self):
        app = Microdot()

        @app.post('/foo/bar')
        async def index(req):
            self.assertEqual(req.app, app)
            self.assertEqual(req.client_addr, ('1.2.3.4', 1234))
            self.assertEqual(req.method, 'POST')
            self.assertEqual(req.http_version, 'HTTP/1.1')
            self.assertEqual(req.path, '/foo/bar')
            self.assertEqual(req.args, {'baz': ['1']})
            self.assertEqual(req.cookies, {'session': 'xyz'})
            self.assertEqual(req.body, b'body')

            class R:
                def __init__(self):
                    self.i = 0
                    self.body = [b're', b'sp', b'on', b'se', b'']

                async def read(self, n):
                    data = self.body[self.i]
                    self.i += 1
                    return data

            return Response(body=R(), headers={'Content-Length': '8'})

        @app.after_request
        def after_request(req, res):
            res.set_cookie('foo', 'foo')
            res.set_cookie('bar', 'bar', http_only=True)

        scope = {
            'type': 'http',
            'path': '/foo/bar',
            'query_string': b'baz=1',
            'headers': [(b'Authorization', b'Bearer 123'),
                        (b'Cookie', b'session=xyz'),
                        (b'Content-Length', b'4')],
            'client': ['1.2.3.4', 1234],
            'method': 'POST',
            'http_version': '1.1',
        }

        event_index = 0

        async def receive():
            nonlocal event_index

            if event_index == 0:
                event_index = 1
                return {
                    'type': 'http.request',
                    'body': b'body',
                    'more_body': False,
                }

            await asyncio.sleep(0.1)
            return {
                'type': 'http.disconnect',
            }

        async def send(packet):
            if packet['type'] == 'http.response.start':
                self.assertEqual(packet['status'], 200)
                expected_headers = [
                    (b'content-length', b'8'),
                    (b'content-type', b'text/plain; charset=UTF-8'),
                    (b'set-cookie', b'foo=foo'),
                    (b'set-cookie', b'bar=bar; HttpOnly')
                ]
                self.assertEqual(len(packet['headers']), len(expected_headers))
                for header in expected_headers:
                    self.assertIn(header, packet['headers'])
            elif packet['type'] == 'http.response.body':
                self.assertIn(packet['body'],
                              [b're', b'sp', b'on', b'se', b''])

        original_buffer_size = Response.send_file_buffer_size
        Response.send_file_buffer_size = 2

        self._run(app(scope, receive, send))

        Response.send_file_buffer_size = original_buffer_size

    def test_wsgi_request_without_query_string(self):
        app = Microdot()

        @app.route('/foo/bar')
        async def index(req):
            self.assertEqual(req.path, '/foo/bar')
            self.assertEqual(req.args, {})
            return 'response'

        scope = {
            'type': 'http',
            'path': '/foo/bar',
            'headers': [(b'Authorization', b'Bearer 123'),
                        (b'Cookie', b'session=xyz'),
                        (b'Content-Length', b'4')],
            'client': ['1.2.3.4', 1234],
            'method': 'POST',
            'http_version': '1.1',
        }

        event_index = 0

        async def receive():
            nonlocal event_index

            if event_index == 0:
                event_index = 1
                return {
                    'type': 'http.request',
                    'body': b'body',
                    'more_body': False,
                }

            await asyncio.sleep(0.1)
            return {
                'type': 'http.disconnect',
            }

        async def send(packet):
            pass

        self._run(app(scope, receive, send))

    def test_shutdown(self):
        app = Microdot()

        @app.route('/shutdown')
        async def shutdown(request):
            request.app.shutdown()

        scope = {
            'type': 'http',
            'path': '/shutdown',
            'client': ['1.2.3.4', 1234],
            'method': 'GET',
            'http_version': '1.1',
        }

        async def receive():
            pass

        async def send(packet):
            pass

        with mock.patch('microdot.asgi.os.kill') as kill:
            self._run(app(scope, receive, send))

        kill.assert_called()
