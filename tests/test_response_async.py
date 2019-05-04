try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

import unittest
from microdot_async import Response
from tests.mock_socket import FakeStreamAsync


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


class TestResponseAsync(unittest.TestCase):
    def test_create_from_string(self):
        res = Response('foo')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {})
        self.assertEqual(res.body, b'foo')
        fd = FakeStreamAsync()
        _run(res.write(fd))
        self.assertIn(b'HTTP/1.0 200 OK\r\n', fd.response)
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nfoo'))

    def test_create_from_string_with_content_length(self):
        res = Response('foo', headers={'Content-Length': '2'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {'Content-Length': '2'})
        self.assertEqual(res.body, b'foo')
        fd = FakeStreamAsync()
        _run(res.write(fd))
        self.assertIn(b'HTTP/1.0 200 OK\r\n', fd.response)
        self.assertIn(b'Content-Length: 2\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nfoo'))

    def test_create_from_bytes(self):
        res = Response(b'foo')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {})
        self.assertEqual(res.body, b'foo')
        fd = FakeStreamAsync()
        _run(res.write(fd))
        self.assertIn(b'HTTP/1.0 200 OK\r\n', fd.response)
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nfoo'))

    def test_create_empty(self):
        res = Response(headers={'X-Foo': 'Bar'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {'X-Foo': 'Bar'})
        self.assertEqual(res.body, b'')
        fd = FakeStreamAsync()
        _run(res.write(fd))
        self.assertIn(b'HTTP/1.0 200 OK\r\n', fd.response)
        self.assertIn(b'X-Foo: Bar\r\n', fd.response)
        self.assertIn(b'Content-Length: 0\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\n'))

    def test_create_json(self):
        res = Response({'foo': 'bar'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {'Content-Type': 'application/json'})
        self.assertEqual(res.body, b'{"foo": "bar"}')
        fd = FakeStreamAsync()
        _run(res.write(fd))
        self.assertIn(b'HTTP/1.0 200 OK\r\n', fd.response)
        self.assertIn(b'Content-Length: 14\r\n', fd.response)
        self.assertIn(b'Content-Type: application/json\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\n{"foo": "bar"}'))

        res = Response([1, '2'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {'Content-Type': 'application/json'})
        self.assertEqual(res.body, b'[1, "2"]')
        fd = FakeStreamAsync()
        _run(res.write(fd))
        self.assertIn(b'HTTP/1.0 200 OK\r\n', fd.response)
        self.assertIn(b'Content-Length: 8\r\n', fd.response)
        self.assertIn(b'Content-Type: application/json\r\n', fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\n[1, "2"]'))
