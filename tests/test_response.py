from datetime import datetime

try:
    import uio as io
except ImportError:
    import io

import unittest
from microdot import Response


class TestResponse(unittest.TestCase):
    def test_create_from_string(self):
        res = Response('foo')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {})
        self.assertEqual(res.body, b'foo')
        fd = io.BytesIO()
        res.write(fd)
        self.assertEqual(
            fd.getvalue(),
            b'HTTP/1.0 200 OK\r\n'
            b'Content-Length: 3\r\n'
            b'Content-Type: text/plain\r\n'
            b'\r\n'
            b'foo')

    def test_create_from_string_with_content_length(self):
        res = Response('foo', headers={'Content-Length': '2'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {'Content-Length': '2'})
        self.assertEqual(res.body, b'foo')
        fd = io.BytesIO()
        res.write(fd)
        self.assertEqual(
            fd.getvalue(),
            b'HTTP/1.0 200 OK\r\n'
            b'Content-Length: 2\r\n'
            b'Content-Type: text/plain\r\n'
            b'\r\n'
            b'foo')

    def test_create_from_bytes(self):
        res = Response(b'foo')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {})
        self.assertEqual(res.body, b'foo')
        fd = io.BytesIO()
        res.write(fd)
        self.assertEqual(
            fd.getvalue(),
            b'HTTP/1.0 200 OK\r\n'
            b'Content-Length: 3\r\n'
            b'Content-Type: text/plain\r\n'
            b'\r\n'
            b'foo')

    def test_create_empty(self):
        res = Response(headers={'X-Foo': 'Bar'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {'X-Foo': 'Bar'})
        self.assertEqual(res.body, b'')
        fd = io.BytesIO()
        res.write(fd)
        self.assertEqual(
            fd.getvalue(),
            b'HTTP/1.0 200 OK\r\n'
            b'X-Foo: Bar\r\n'
            b'Content-Length: 0\r\n'
            b'Content-Type: text/plain\r\n'
            b'\r\n')

    def test_create_json(self):
        res = Response({'foo': 'bar'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {'Content-Type': 'application/json'})
        self.assertEqual(res.body, b'{"foo": "bar"}')
        fd = io.BytesIO()
        res.write(fd)
        self.assertEqual(
            fd.getvalue(),
            b'HTTP/1.0 200 OK\r\n'
            b'Content-Type: application/json\r\n'
            b'Content-Length: 14\r\n'
            b'\r\n'
            b'{"foo": "bar"}')

        res = Response([1, '2'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {'Content-Type': 'application/json'})
        self.assertEqual(res.body, b'[1, "2"]')
        fd = io.BytesIO()
        res.write(fd)
        self.assertEqual(
            fd.getvalue(),
            b'HTTP/1.0 200 OK\r\n'
            b'Content-Type: application/json\r\n'
            b'Content-Length: 8\r\n'
            b'\r\n'
            b'[1, "2"]')

    def test_create_from_other(self):
        res = Response(123)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {})
        self.assertEqual(res.body, b'123')

    def test_create_with_status_code(self):
        res = Response('not found', 404)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.headers, {})
        self.assertEqual(res.body, b'not found')

    def test_create_with_headers(self):
        res = Response('foo', headers={'X-Test': 'Foo'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {'X-Test': 'Foo'})
        self.assertEqual(res.body, b'foo')

    def test_create_with_status_code_and_headers(self):
        res = Response('foo', 202, {'X-Test': 'Foo'})
        self.assertEqual(res.status_code, 202)
        self.assertEqual(res.headers, {'X-Test': 'Foo'})
        self.assertEqual(res.body, b'foo')

    def test_cookies(self):
        res = Response('ok')
        res.set_cookie('foo1', 'bar1')
        res.set_cookie('foo2', 'bar2', path='/')
        res.set_cookie('foo3', 'bar3', domain='example.com:1234')
        res.set_cookie('foo4', 'bar4',
                       expires=datetime(2019, 11, 5, 2, 23, 54))
        res.set_cookie('foo5', 'bar5', max_age=123)
        res.set_cookie('foo6', 'bar6', secure=True, http_only=True)
        res.set_cookie('foo7', 'bar7', path='/foo', domain='example.com:1234',
                       expires=datetime(2019, 11, 5, 2, 23, 54), max_age=123,
                       secure=True, http_only=True)
        self.assertEqual(res.headers, {'Set-Cookie': [
            'foo1=bar1',
            'foo2=bar2; Path=/',
            'foo3=bar3; Domain=example.com:1234',
            'foo4=bar4; Expires=Tue, 05 Nov 2019 02:23:54 GMT',
            'foo5=bar5; Max-Age=123',
            'foo6=bar6; Secure; HttpOnly',
            'foo7=bar7; Path=/foo; Domain=example.com:1234; '
            'Expires=Tue, 05 Nov 2019 02:23:54 GMT; Max-Age=123; Secure; '
            'HttpOnly'
        ]})

    def test_redirect(self):
        res = Response.redirect('/foo')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers['Location'], '/foo')

        res = Response.redirect('/foo', status_code=301)
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers['Location'], '/foo')

    def test_send_file(self):
        files = [
            ('test.txt', 'text/plain'),
            ('test.gif', 'image/gif'),
            ('test.jpg', 'image/jpeg'),
            ('test.png', 'image/png'),
            ('test.html', 'text/html'),
            ('test.css', 'text/css'),
            ('test.js', 'application/javascript'),
            ('test.json', 'application/json'),
            ('test.bin', 'application/octet-stream'),
        ]
        for file, content_type in files:
            res = Response.send_file('tests/files/' + file)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.headers['Content-Type'], content_type)
            self.assertEqual(res.headers['Content-Length'], '4')
            self.assertEqual(res.body, b'foo\n')
        res = Response.send_file('tests/files/test.txt',
                                 content_type='text/html')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'text/html')
        self.assertEqual(res.headers['Content-Length'], '4')
        self.assertEqual(res.body, b'foo\n')
