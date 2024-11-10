import asyncio
import unittest
from microdot import Response
from tests.mock_socket import FakeStreamAsync


class TestResponse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if hasattr(asyncio, 'set_event_loop'):
            asyncio.set_event_loop(asyncio.new_event_loop())
        cls.loop = asyncio.get_event_loop()

    def _run(self, coro):
        return self.loop.run_until_complete(coro)

    def test_create_from_string(self):
        res = Response('foo')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {})
        self.assertEqual(res.body, b'foo')
        fd = FakeStreamAsync()
        self._run(res.write(fd))
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
        self._run(res.write(fd))
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
        self._run(res.write(fd))
        self.assertIn(b'HTTP/1.0 200 OK\r\n', fd.response)
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain; charset=UTF-8\r\n',
                      fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nfoo'))

    def test_create_from_head(self):
        res = Response(b'foo')
        res.is_head = True
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {})
        self.assertEqual(res.body, b'foo')
        fd = FakeStreamAsync()
        self._run(res.write(fd))
        self.assertIn(b'HTTP/1.0 200 OK\r\n', fd.response)
        self.assertIn(b'Content-Length: 3\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain; charset=UTF-8\r\n',
                      fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\n'))
        self.assertFalse(b'foo' in fd.response)

    def test_create_empty(self):
        res = Response(headers={'X-Foo': 'Bar'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {'X-Foo': 'Bar'})
        self.assertEqual(res.body, b'')
        fd = FakeStreamAsync()
        self._run(res.write(fd))
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
        self._run(res.write(fd))
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
        self._run(res.write(fd))
        self.assertIn(b'HTTP/1.0 200 OK\r\n', fd.response)
        self.assertIn(b'Content-Length: 8\r\n', fd.response)
        self.assertIn(b'Content-Type: application/json; charset=UTF-8\r\n',
                      fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\n[1, "2"]'))

    def test_create_from_none(self):
        res = Response(None)
        self.assertEqual(res.status_code, 204)
        self.assertEqual(res.body, b'')
        fd = FakeStreamAsync()
        self._run(res.write(fd))
        self.assertIn(b'HTTP/1.0 204 N/A\r\n', fd.response)
        self.assertIn(b'Content-Length: 0\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain; charset=UTF-8\r\n',
                      fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\n'))

    def test_create_from_iterator(self):
        def gen():
            yield 'foo'
            yield 'bar'

        res = Response(gen())
        fd = FakeStreamAsync()
        self._run(res.write(fd))
        print(fd.response)
        self.assertIn(b'HTTP/1.0 200 OK\r\n', fd.response)
        self.assertIn(b'Content-Type: text/plain; charset=UTF-8\r\n',
                      fd.response)
        self.assertTrue(fd.response.endswith(b'\r\n\r\nfoobar'))

    def test_create_from_other(self):
        res = Response(23.7)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {})
        self.assertEqual(res.body, 23.7)

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

    def test_create_with_reason(self):
        res = Response('foo', reason='ALL GOOD!')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers, {})
        self.assertEqual(res.reason, 'ALL GOOD!')
        self.assertEqual(res.body, b'foo')
        fd = FakeStreamAsync()
        self._run(res.write(fd))
        self.assertIn(b'HTTP/1.0 200 ALL GOOD!\r\n', fd.response)

    def test_create_with_status_and_reason(self):
        res = Response('not found', 404, reason='NOT FOUND')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.headers, {})
        self.assertEqual(res.reason, 'NOT FOUND')
        self.assertEqual(res.body, b'not found')
        fd = FakeStreamAsync()
        self._run(res.write(fd))
        self.assertIn(b'HTTP/1.0 404 NOT FOUND\r\n', fd.response)

    def test_cookies(self):
        res = Response('ok')
        res.set_cookie('foo1', 'bar1')
        res.set_cookie('foo2', 'bar2', path='/', partitioned=True)
        res.set_cookie('foo3', 'bar3', domain='example.com:1234')
        res.set_cookie('foo4', 'bar4',
                       expires='Tue, 05 Nov 2019 02:23:54 GMT')
        res.set_cookie('foo5', 'bar5', max_age=123,
                       expires='Thu, 01 Jan 1970 00:00:00 GMT')
        res.set_cookie('foo6', 'bar6', secure=True, http_only=True)
        res.set_cookie('foo7', 'bar7', path='/foo', domain='example.com:1234',
                       expires='Tue, 05 Nov 2019 02:23:54 GMT', max_age=123,
                       secure=True, http_only=True)
        res.delete_cookie('foo8', http_only=True)
        res.delete_cookie('foo9', path='/s')
        self.assertEqual(res.headers, {'Set-Cookie': [
            'foo1=bar1',
            'foo2=bar2; Path=/; Partitioned',
            'foo3=bar3; Domain=example.com:1234',
            'foo4=bar4; Expires=Tue, 05 Nov 2019 02:23:54 GMT',
            'foo5=bar5; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=123',
            'foo6=bar6; Secure; HttpOnly',
            'foo7=bar7; Path=/foo; Domain=example.com:1234; '
            'Expires=Tue, 05 Nov 2019 02:23:54 GMT; Max-Age=123; Secure; '
            'HttpOnly',
            ('foo8=; Expires=Thu, 01 Jan 1970 00:00:01 GMT; Max-Age=0; '
             'HttpOnly'),
            ('foo9=; Path=/s; Expires=Thu, 01 Jan 1970 00:00:01 GMT; '
             'Max-Age=0'),
        ]})

    def test_redirect(self):
        res = Response.redirect('/foo')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers['Location'], '/foo')

        res = Response.redirect('/foo', status_code=301)
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers['Location'], '/foo')

        with self.assertRaises(ValueError):
            Response.redirect('/foo\x0d\x0a\x0d\x0a<p>Foo</p>')

    def test_send_file(self):
        res = Response.send_file('tests/files/test.txt',
                                 content_type='text/html')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'text/html')
        fd = FakeStreamAsync()
        self._run(res.write(fd))
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
        self._run(res.write(fd))
        self.assertEqual(
            fd.response,
            b'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\nfoo\n')
        Response.send_file_buffer_size = original_buffer_size

    def test_send_file_max_age(self):
        res = Response.send_file('tests/files/test.txt', max_age=123)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Cache-Control'], 'max-age=123')

        Response.default_send_file_max_age = 456
        res = Response.send_file('tests/files/test.txt')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Cache-Control'], 'max-age=456')
        res = Response.send_file('tests/files/test.txt', max_age=123)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Cache-Control'], 'max-age=123')

        Response.default_send_file_max_age = None

    def test_send_file_compressed(self):
        res = Response.send_file('tests/files/test.txt', compressed=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'text/plain')
        self.assertEqual(res.headers['Content-Encoding'], 'gzip')

        res = Response.send_file('tests/files/test.txt', compressed='foo')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'text/plain')
        self.assertEqual(res.headers['Content-Encoding'], 'foo')

        res = Response.send_file('tests/files/test', compressed=True,
                                 file_extension='.gz')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'application/octet-stream')
        self.assertEqual(res.headers['Content-Encoding'], 'gzip')

    def test_send_file_gzip_handling(self):
        res = Response.send_file('tests/files/test.txt.gz')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'],
                         'application/octet-stream')

        res = Response.send_file('tests/files/test.txt.gz', compressed=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'text/plain')
        self.assertEqual(res.headers['Content-Encoding'], 'gzip')

    def test_default_content_type(self):
        original_content_type = Response.default_content_type
        res = Response('foo')
        res.complete()
        self.assertEqual(res.headers['Content-Type'],
                         'text/plain; charset=UTF-8')
        Response.default_content_type = 'text/html'
        res = Response('foo')
        res.complete()
        self.assertEqual(res.headers['Content-Type'],
                         'text/html; charset=UTF-8')
        Response.default_content_type = 'text/html; charset=ISO-8859-1'
        res = Response('foo')
        res.complete()
        self.assertEqual(res.headers['Content-Type'],
                         'text/html; charset=ISO-8859-1')
        Response.default_content_type = original_content_type
