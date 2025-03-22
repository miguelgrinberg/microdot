import asyncio
import os
import unittest
from microdot import Microdot
from microdot.multipart import with_form_data, FileUpload, FormDataIter
from microdot.test_client import TestClient


class TestMultipart(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if hasattr(asyncio, 'set_event_loop'):
            asyncio.set_event_loop(asyncio.new_event_loop())
        cls.loop = asyncio.get_event_loop()

    def _run(self, coro):
        return self.loop.run_until_complete(coro)

    def test_simple_form(self):
        app = Microdot()

        @app.post('/sync')
        @with_form_data
        def sync_route(req):
            return dict(req.form)

        @app.post('/async')
        @with_form_data
        async def async_route(req):
            return dict(req.form)

        client = TestClient(app)

        res = self._run(client.post(
            '/sync', headers={
                'Content-Type': 'multipart/form-data; boundary=boundary',
            },
            body=(
                b'--boundary\r\n'
                b'Content-Disposition: form-data; name="foo"\r\n\r\nbar\r\n'
                b'--boundary\r\n'
                b'Content-Disposition: form-data; name="baz"\r\n\r\nbaz\r\n'
                b'--boundary--\r\n')
        ))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'foo': 'bar', 'baz': 'baz'})

        res = self._run(client.post(
            '/async', headers={
                'Content-Type': 'multipart/form-data; boundary=boundary',
            },
            body=(
                b'--boundary\r\n'
                b'Content-Disposition: form-data; name="foo"\r\n\r\nbar\r\n'
                b'--boundary\r\n'
                b'Content-Disposition: form-data; name="baz"\r\n\r\nbaz\r\n'
                b'--boundary--\r\n')
        ))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'foo': 'bar', 'baz': 'baz'})

    def test_form_with_files(self):
        saved_max_memory_size = FileUpload.max_memory_size
        FileUpload.max_memory_size = 5

        app = Microdot()

        @app.post('/async')
        @with_form_data
        async def async_route(req):
            d = dict(req.form)
            for name, file in req.files.items():
                d[name] = '{}|{}|{}'.format(file.filename, file.content_type,
                                            (await file.read()).decode())
            return d

        client = TestClient(app)

        res = self._run(client.post(
            '/async', headers={
                'Content-Type': 'multipart/form-data; boundary=boundary',
            },
            body=(
                b'--boundary\r\n'
                b'Content-Disposition: form-data; name="foo"\r\n\r\nbar\r\n'
                b'--boundary\r\n'
                b'Content-Disposition: form-data; name="f"; filename="f"\r\n'
                b'Content-Type: text/plain\r\n\r\nbaz\r\n'
                b'--boundary\r\n'
                b'Content-Disposition: form-data; name="g"; filename="g"\r\n'
                b'Content-Type: text/html\r\n\r\n<p>hello</p>\r\n'
                b'--boundary\r\n'
                b'Content-Disposition: form-data; name="x"\r\n\r\ny\r\n'
                b'--boundary--\r\n')
        ))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'foo': 'bar', 'x': 'y',
                                    'f': 'f|text/plain|baz',
                                    'g': 'g|text/html|<p>hello</p>'})
        FileUpload.max_memory_size = saved_max_memory_size

    def test_file_save(self):
        app = Microdot()

        @app.post('/async')
        @with_form_data
        async def async_route(req):
            for _, file in req.files.items():
                await file.save('_x.txt')

        client = TestClient(app)

        res = self._run(client.post(
            '/async', headers={
                'Content-Type': 'multipart/form-data; boundary=boundary',
            },
            body=(
                b'--boundary\r\n'
                b'Content-Disposition: form-data; name="foo"\r\n\r\nbar\r\n'
                b'--boundary\r\n'
                b'Content-Disposition: form-data; name="f"; filename="f"\r\n'
                b'Content-Type: text/plain\r\n\r\nbaz\r\n'
                b'--boundary--\r\n')
        ))
        self.assertEqual(res.status_code, 204)
        with open('_x.txt', 'rb') as f:
            self.assertEqual(f.read(), b'baz')
        os.unlink('_x.txt')

    def test_no_form(self):
        app = Microdot()

        @app.post('/async')
        @with_form_data
        async def async_route(req):
            return str(req.form)

        client = TestClient(app)

        res = self._run(client.post('/async', body={'foo': 'bar'}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, 'None')

    def test_upload_iterator(self):
        app = Microdot()

        @app.post('/async')
        async def async_route(req):
            d = {}
            async for name, value in FormDataIter(req):
                if isinstance(value, FileUpload):
                    d[name] = '{}|{}|{}'.format(value.filename,
                                                value.content_type,
                                                (await value.read(4)).decode())
                else:
                    d[name] = value
            return d

        client = TestClient(app)

        res = self._run(client.post(
            '/async', headers={
                'Content-Type': 'multipart/form-data; boundary=boundary',
            },
            body=(
                b'--boundary\r\n'
                b'Content-Disposition: form-data; name="foo"\r\n\r\nbar\r\n'
                b'--boundary\r\n'
                b'Content-Disposition: form-data; name="f"; filename="f"\r\n'
                b'Content-Type: text/plain\r\n\r\nbaz\r\n'
                b'--boundary\r\n'
                b'Content-Disposition: form-data; name="g"; filename="g.h"\r\n'
                b'Content-Type: text/html\r\n\r\n<p>hello</p>\r\n'
                b'--boundary\r\n'
                b'Content-Disposition: form-data; name="x"\r\n\r\ny\r\n'
                b'--boundary\r\n'
                b'Content-Disposition: form-data; name="h"; filename="hh"\r\n'
                b'Content-Type: text/plain\r\n\r\nyy' + (b'z' * 500) + b'\r\n'
                b'--boundary\r\n'
                b'Content-Disposition: form-data; name="i"; filename="i.1"\r\n'
                b'Content-Type: text/plain\r\n\r\n1234\r\n'
                b'--boundary--\r\n')
        ))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {
            'foo': 'bar',
            'f': 'f|text/plain|baz',
            'g': 'g.h|text/html|<p>h',
            'x': 'y',
            'h': 'hh|text/plain|yyzz',
            'i': 'i.1|text/plain|1234',
        })
