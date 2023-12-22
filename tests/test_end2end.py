import asyncio
import sys
import time
import unittest
from microdot import Microdot


class TestEnd2End(unittest.TestCase):
    async def request(self, url, method='GET'):
        while True:
            reader, writer = await asyncio.open_connection('localhost', 5678)
            try:
                writer.write(f'{method} {url} HTTP/1.0\r\n\r\n'.encode())
                break
            except OSError:
                # micropython's server sometimes needs a moment
                writer.close()
                await writer.wait_closed()
                await asyncio.sleep(0.1)
        await writer.drain()

        response = await reader.read()
        writer.close()
        await writer.wait_closed()
        return response.decode().splitlines()

    def test_get(self):
        app = Microdot()

        @app.route('/')
        def index(request):
            return 'Hello, World!'

        @app.route('/shutdown')
        def shutdown(request):
            app.shutdown()
            return ''

        async def run():
            server = asyncio.create_task(app.start_server(host='127.0.0.1',
                                                          port=5678))
            await asyncio.sleep(0.1)
            response = await self.request('/')
            self.assertEqual(response[0], 'HTTP/1.0 200 OK')
            self.assertEqual(response[-1], 'Hello, World!')
            await self.request('/shutdown')
            await server

        asyncio.run(run())

    @unittest.skipIf(sys.implementation.name == 'micropython',
                     'not supported under MicroPython')
    def test_concurrent_requests(self):
        app = Microdot()
        counter = 0

        @app.route('/async1')
        async def async1(request):
            nonlocal counter
            counter += 1
            while counter < 4:
                await asyncio.sleep(0.01)
            return 'OK'

        @app.route('/async2')
        async def async2(request):
            nonlocal counter
            counter += 1
            while counter < 4:
                await asyncio.sleep(0.01)
            return 'OK'

        @app.route('/sync1')
        def sync1(request):
            nonlocal counter
            counter += 1
            while counter < 4:
                time.sleep(0.01)
            return 'OK'

        @app.route('/sync2')
        def sync2(request):
            nonlocal counter
            counter += 1
            while counter < 4:
                time.sleep(0.01)
            return 'OK'

        @app.route('/shutdown')
        def shutdown(request):
            app.shutdown()
            return ''

        async def run():
            server = asyncio.create_task(app.start_server(port=5678))
            await asyncio.sleep(0.1)
            await asyncio.gather(self.request('/async1'),
                                 self.request('/async2'),
                                 self.request('/sync1'),
                                 self.request('/sync2'))
            await self.request('/shutdown')
            await server

        asyncio.run(run())
