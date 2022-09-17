try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

import unittest
from microdot_asyncio import Response
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
        self.assertIn(b'Content-Type: text/plain; charset=UTF-8\r\n',
                      fd.response)
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
        self.assertIn(b'Content-Type: text/plain; charset=UTF-8\r\n',
                      fd.response)
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
        self.assertIn(b'Content-Type: text/plain; charset=UTF-8\r\n',
                      fd.response)
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
        self.assertIn(b'Content-Type: text/plain; charset=UTF-8\r\n',
                      fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\n'))

    def test_create_json(self):
        res = Response({'foo': 'bar'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers,
                         {'Content-Type': 'application/json; charset=UTF-8'})
        self.assertEqual(res.body, b'{"foo": "bar"}')
        fd = FakeStreamAsync()
        _run(res.write(fd))
        self.assertIn(b'HTTP/1.0 200 OK\r\n', fd.response)
        self.assertIn(b'Content-Length: 14\r\n', fd.response)
        self.assertIn(b'Content-Type: application/json; charset=UTF-8\r\n',
                      fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\n{"foo": "bar"}'))

        res = Response([1, '2'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers,
                         {'Content-Type': 'application/json; charset=UTF-8'})
        self.assertEqual(res.body, b'[1, "2"]')
        fd = FakeStreamAsync()
        _run(res.write(fd))
        self.assertIn(b'HTTP/1.0 200 OK\r\n', fd.response)
        self.assertIn(b'Content-Length: 8\r\n', fd.response)
        self.assertIn(b'Content-Type: application/json; charset=UTF-8\r\n',
                      fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\n[1, "2"]'))

    def test_create_with_reason(self):
        res = Response('foo', reason='ALL GOOD!')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {})
        self.assertEqual(res.reason, 'ALL GOOD!')
        self.assertEqual(res.body, b'foo')
        fd = FakeStreamAsync()
        _run(res.write(fd))
        self.assertIn(b'HTTP/1.0 200 ALL GOOD!\r\n', fd.response)

    def test_create_with_status_and_reason(self):
        res = Response('not found', 404, reason='NOT FOUND')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.headers, {})
        self.assertEqual(res.reason, 'NOT FOUND')
        self.assertEqual(res.body, b'not found')
        fd = FakeStreamAsync()
        _run(res.write(fd))
        self.assertIn(b'HTTP/1.0 404 NOT FOUND\r\n', fd.response)

    def test_send_file(self):
        res = Response.send_file('tests/files/test.txt',
                                 content_type='text/html')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'text/html')
        fd = FakeStreamAsync()
        _run(res.write(fd))
        self.assertEqual(
            fd.response,
            b'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\nfoo\n')

    def test_send_file_small_buffer(self):
        original_buffer_size = Response.send_file_buffer_size
        Response.send_file_buffer_size = 2
        res = Response.send_file('tests/files/test.txt',
                                 content_type='text/html')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'text/html')
        fd = FakeStreamAsync()
        _run(res.write(fd))
        self.assertEqual(
            fd.response,
            b'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\nfoo\n')
        Response.send_file_buffer_size = original_buffer_size
