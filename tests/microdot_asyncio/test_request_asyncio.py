try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

import unittest
from microdot import MultiDict
from microdot_asyncio import Request
from tests.mock_socket import get_async_request_fd


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


class TestRequestAsync(unittest.TestCase):
    def test_create_request(self):
        fd = get_async_request_fd('GET', '/foo')
        req = _run(Request.create('app', fd, 'addr'))
        self.assertEqual(req.app, 'app')
        self.assertEqual(req.client_addr, 'addr')
        self.assertEqual(req.method, 'GET')
        self.assertEqual(req.path, '/foo')
        self.assertEqual(req.http_version, '1.0')
        self.assertIsNone(req.query_string)
        self.assertEqual(req.args, {})
        self.assertEqual(req.headers, {'Host': 'example.com:1234'})
        self.assertEqual(req.cookies, {})
        self.assertEqual(req.content_length, 0)
        self.assertEqual(req.content_type, None)
        self.assertEqual(req.body, b'')
        self.assertEqual(req.json, None)
        self.assertEqual(req.form, None)

    def test_headers(self):
        fd = get_async_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/json',
            'Cookie': 'foo=bar;abc=def',
            'Content-Length': '3'}, body='aaa')
        req = _run(Request.create('app', fd, 'addr'))
        self.assertEqual(req.headers, {
            'Host': 'example.com:1234',
            'Content-Type': 'application/json',
            'Cookie': 'foo=bar;abc=def',
            'Content-Length': '3'})
        self.assertEqual(req.content_type, 'application/json')
        self.assertEqual(req.cookies, {'foo': 'bar', 'abc': 'def'})
        self.assertEqual(req.content_length, 3)
        self.assertEqual(req.body, b'aaa')

    def test_args(self):
        fd = get_async_request_fd('GET', '/?foo=bar&abc=def&x=%2f%%')
        req = _run(Request.create('app', fd, 'addr'))
        self.assertEqual(req.query_string, 'foo=bar&abc=def&x=%2f%%')
        self.assertEqual(req.args, MultiDict(
            {'foo': 'bar', 'abc': 'def', 'x': '/%%'}))

    def test_json(self):
        fd = get_async_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/json'}, body='{"foo":"bar"}')
        req = _run(Request.create('app', fd, 'addr'))
        json = req.json
        self.assertEqual(json, {'foo': 'bar'})
        self.assertTrue(req.json is json)

        fd = get_async_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/json'}, body='[1, "2"]')
        req = _run(Request.create('app', fd, 'addr'))
        self.assertEqual(req.json, [1, '2'])

        fd = get_async_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/xml'}, body='[1, "2"]')
        req = _run(Request.create('app', fd, 'addr'))
        self.assertIsNone(req.json)

    def test_form(self):
        fd = get_async_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/x-www-form-urlencoded'},
            body='foo=bar&abc=def&x=%2f%%')
        req = _run(Request.create('app', fd, 'addr'))
        form = req.form
        self.assertEqual(form, MultiDict(
            {'foo': 'bar', 'abc': 'def', 'x': '/%%'}))
        self.assertTrue(req.form is form)

        fd = get_async_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/json'},
            body='foo=bar&abc=def&x=%2f%%')
        req = _run(Request.create('app', fd, 'addr'))
        self.assertIsNone(req.form)

    def test_large_payload(self):
        saved_max_content_length = Request.max_content_length
        Request.max_content_length = 16

        fd = get_async_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/x-www-form-urlencoded'},
            body='foo=bar&abc=def&x=y')
        req = _run(Request.create('app', fd, 'addr'))
        assert req.body == b''

        Request.max_content_length = saved_max_content_length
