try:
    import uio as io
except ImportError:
    import io

import unittest
from microdot import Request


class TestRequest(unittest.TestCase):
    def _get_request_fd(self, method, path, headers=None, body=None):
        if headers is None:
            headers = {}
        if body is None:
            body = ''
        elif 'Content-Length' not in headers:
            headers['Content-Length'] = str(len(body))
        request_bytes = '{method} {path} HTTP/1.0\n'.format(
            method=method, path=path)
        if 'Host' not in headers:
            headers['Host'] = 'example.com:1234'
        for header, value in headers.items():
            request_bytes += '{header}: {value}\n'.format(
                header=header, value=value)
        request_bytes += '\n' + body
        return io.BytesIO(request_bytes.encode())

    def test_create_request(self):
        fd = self._get_request_fd('GET', '/foo')
        req = Request(fd, 'addr')
        req.close()
        self.assertEqual(req.client_sock, fd)
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
        fd = self._get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/json',
            'Cookie': 'foo=bar;abc=def',
            'Content-Length': '3'}, body='aaa')
        req = Request(fd, 'addr')
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
        fd = self._get_request_fd('GET', '/?foo=bar&abc=def&x=%2f%%')
        req = Request(fd, 'addr')
        self.assertEqual(req.query_string, 'foo=bar&abc=def&x=%2f%%')
        self.assertEqual(req.args, {'foo': 'bar', 'abc': 'def', 'x': '/%%'})

    def test_json(self):
        fd = self._get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/json'}, body='{"foo":"bar"}')
        req = Request(fd, 'addr')
        self.assertEqual(req.json, {'foo': 'bar'})

        fd = self._get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/json'}, body='[1, "2"]')
        req = Request(fd, 'addr')
        self.assertEqual(req.json, [1, '2'])

        fd = self._get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/xml'}, body='[1, "2"]')
        req = Request(fd, 'addr')
        self.assertIsNone(req.json)

    def test_form(self):
        fd = self._get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/x-www-form-urlencoded'},
            body='foo=bar&abc=def&x=%2f%%')
        req = Request(fd, 'addr')
        self.assertEqual(req.form, {'foo': 'bar', 'abc': 'def', 'x': '/%%'})

        fd = self._get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/json'},
            body='foo=bar&abc=def&x=%2f%%')
        req = Request(fd, 'addr')
        self.assertIsNone(req.form)
