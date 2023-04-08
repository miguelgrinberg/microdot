import unittest
from microdot import Request, MultiDict
from tests.mock_socket import get_request_fd


class TestRequest(unittest.TestCase):
    def test_create_request(self):
        fd = get_request_fd('GET', '/foo')
        req = Request.create('app', fd, 'addr')
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
        fd = get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/json',
            'Cookie': 'foo=bar;abc=def',
            'Content-Length': '3'}, body='aaa')
        req = Request.create('app', fd, 'addr')
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
        req = Request.create('app', fd, 'addr')
        self.assertEqual(req.query_string, 'foo=bar&abc=def&x=%2f%%')
        self.assertEqual(req.args, MultiDict(
            {'foo': 'bar', 'abc': 'def', 'x': '/%%'}))

    def test_badly_formatted_args(self):
        fd = get_request_fd('GET', '/?&foo=bar&abc=def&&&x=%2f%%')
        req = Request.create('app', fd, 'addr')
        self.assertEqual(req.query_string, '&foo=bar&abc=def&&&x=%2f%%')
        self.assertEqual(req.args, MultiDict(
            {'foo': 'bar', 'abc': 'def', 'x': '/%%'}))

    def test_json(self):
        fd = get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/json'}, body='{"foo":"bar"}')
        req = Request.create('app', fd, 'addr')
        json = req.json
        self.assertEqual(json, {'foo': 'bar'})
        self.assertTrue(req.json is json)

        fd = get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/json'}, body='[1, "2"]')
        req = Request.create('app', fd, 'addr')
        self.assertEqual(req.json, [1, '2'])

        fd = get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/xml'}, body='[1, "2"]')
        req = Request.create('app', fd, 'addr')
        self.assertIsNone(req.json)

    def test_form(self):
        fd = get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/x-www-form-urlencoded'},
            body='foo=bar&abc=def&x=%2f%%')
        req = Request.create('app', fd, 'addr')
        form = req.form
        self.assertEqual(form, MultiDict(
            {'foo': 'bar', 'abc': 'def', 'x': '/%%'}))
        self.assertTrue(req.form is form)

        fd = get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/x-www-form-urlencoded'},
            body='')
        req = Request.create('app', fd, 'addr')
        form = req.form
        self.assertEqual(form, MultiDict({}))
        self.assertTrue(req.form is form)

        fd = get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/json'},
            body='foo=bar&abc=def&x=%2f%%')
        req = Request.create('app', fd, 'addr')
        self.assertIsNone(req.form)

    def test_large_line(self):
        saved_max_readline = Request.max_readline
        Request.max_readline = 16

        fd = get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/x-www-form-urlencoded'},
            body='foo=bar&abc=def&x=y')
        with self.assertRaises(ValueError):
            Request.create('app', fd, 'addr')

        Request.max_readline = saved_max_readline

    def test_stream(self):
        fd = get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '19'},
            body='foo=bar&abc=def&x=y')
        req = Request.create('app', fd, 'addr')
        self.assertEqual(req.stream.read(), b'foo=bar&abc=def&x=y')
        with self.assertRaises(RuntimeError):
            req.body

    def test_body(self):
        fd = get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '19'},
            body='foo=bar&abc=def&x=y')
        req = Request.create('app', fd, 'addr')
        self.assertEqual(req.body, b'foo=bar&abc=def&x=y')
        with self.assertRaises(RuntimeError):
            req.stream

    def test_large_payload(self):
        saved_max_content_length = Request.max_content_length
        saved_max_body_length = Request.max_body_length
        Request.max_content_length = 32
        Request.max_body_length = 16

        fd = get_request_fd('GET', '/foo', headers={
            'Content-Type': 'application/x-www-form-urlencoded'},
            body='foo=bar&abc=def&x=y')
        req = Request.create('app', fd, 'addr')
        self.assertEqual(req.body, b'')
        self.assertEqual(req.stream.read(), b'foo=bar&abc=def&x=y')

        Request.max_content_length = saved_max_content_length
        Request.max_body_length = saved_max_body_length
