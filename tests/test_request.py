import unittest
from microdot import Request
from tests.mock_socket import get_request_fd


class TestRequest(unittest.TestCase):
    def test_create_request(self):
        fd = get_request_fd('GET', '/foo')
        req = Request.create(fd, 'addr')
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
        fd = get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/json',
            'Cookie': 'foo=bar;abc=def',
            'Content-Length': '3'}, body='aaa')
        req = Request.create(fd, 'addr')
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
        fd = get_request_fd('GET', '/?foo=bar&abc=def&x=%2f%%')
        req = Request.create(fd, 'addr')
        self.assertEqual(req.query_string, 'foo=bar&abc=def&x=%2f%%')
        self.assertEqual(req.args, {'foo': 'bar', 'abc': 'def', 'x': '/%%'})

    def test_json(self):
        fd = get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/json'}, body='{"foo":"bar"}')
        req = Request.create(fd, 'addr')
        json = req.json
        self.assertEqual(json, {'foo': 'bar'})
        self.assertTrue(req.json is json)

        fd = get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/json'}, body='[1, "2"]')
        req = Request.create(fd, 'addr')
        self.assertEqual(req.json, [1, '2'])

        fd = get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/xml'}, body='[1, "2"]')
        req = Request.create(fd, 'addr')
        self.assertIsNone(req.json)

    def test_form(self):
        fd = get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/x-www-form-urlencoded'},
            body='foo=bar&abc=def&x=%2f%%')
        req = Request.create(fd, 'addr')
        form = req.form
        self.assertEqual(form, {'foo': 'bar', 'abc': 'def', 'x': '/%%'})
        self.assertTrue(req.form is form)

        fd = get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/json'},
            body='foo=bar&abc=def&x=%2f%%')
        req = Request.create(fd, 'addr')
        self.assertIsNone(req.form)
