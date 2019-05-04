try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
from microdot import Microdot as BaseMicrodot
from microdot import print_exception
from microdot import Request as BaseRequest
from microdot import Response as BaseResponse


class Request(BaseRequest):
    @staticmethod
    async def create(stream, client_addr):
        # request line
        line = (await stream.readline()).strip().decode()
        method, url, http_version = line.split()
        http_version = http_version.split('/', 1)[1]

        # headers
        headers = {}
        content_length = 0
        while True:
            line = (await stream.readline()).strip().decode()
            if line == '':
                break
            header, value = line.split(':', 1)
            value = value.strip()
            headers[header] = value
            if header == 'Content-Length':
                content_length = int(value)

        # body
        body = await stream.read(content_length) \
            if content_length else b''

        return Request(client_addr, method, url, http_version, headers, body)


class Response(BaseResponse):
    async def write(self, stream):
        self.complete()

        # status code
        await stream.awrite('HTTP/1.0 {status_code} {reason}\r\n'.format(
            status_code=self.status_code,
            reason='OK' if self.status_code == 200 else 'N/A').encode())

        # headers
        for header, value in self.headers.items():
            values = value if isinstance(value, list) else [value]
            for value in values:
                await stream.awrite('{header}: {value}\r\n'.format(
                    header=header, value=value).encode())
        await stream.awrite(b'\r\n')

        # body
        if self.body:
            await stream.awrite(self.body)


class Microdot(BaseMicrodot):
    def run(self, host='0.0.0.0', port=5000, debug=False):
        async def serve(reader, writer):
            req = await Request.create(reader,
                                       writer.get_extra_info('peername'))
            res = await self.dispatch_request(req)
            if debug:  # pragma: no cover
                print('{method} {path} {status_code}'.format(
                    method=req.method, path=req.path,
                    status_code=res.status_code))

            if not hasattr(writer, 'awrite'):
                class AWriter:
                    def __init__(self, writer):
                        self.writer = writer

                    async def awrite(self, data):
                        self.writer.write(data)
                        await self.writer.drain()

                    async def aclose(self):
                        self.writer.close()

                writer = AWriter(writer)
            await res.write(writer)
            await writer.aclose()

        if debug:  # pragma: no cover
            print('Listening on {host}:{port}...'.format(host=host, port=port))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.start_server(serve, host, port))
        loop.run_forever()
        loop.close()

    async def dispatch_request(self, req):
        f = self.find_route(req)
        try:
            res = None
            if f:
                for handler in self.before_request_handlers:
                    res = await self._invoke_handler(handler, req)
                    if res:
                        break
                if res is None:
                    res = await self._invoke_handler(f, req, **req.url_args)
                if isinstance(res, tuple):
                    res = Response(*res)
                elif not isinstance(res, Response):
                    res = Response(res)
                for handler in self.after_request_handlers:
                    res = await self._invoke_handler(handler, req, res) or res
            elif 404 in self.error_handlers:
                res = self._invoke_handler(self.error_handlers[404], req)
            else:
                res = 'Not found', 404
        except Exception as exc:
            print_exception(exc)
            res = None
            if exc.__class__ in self.error_handlers:
                try:
                    res = self._invoke_handler(
                        self.error_handlers[exc.__class__], req, exc)
                except Exception as exc2:  # pragma: no cover
                    print_exception(exc2)
            if res is None:
                if 500 in self.error_handlers:
                    res = await self._invoke_handler(self.error_handlers[500],
                                                     req)
                else:
                    res = 'Internal server error', 500
        if isinstance(res, tuple):
            res = Response(*res)
        elif not isinstance(res, Response):
            res = Response(res)
        return res

    async def _invoke_handler(self, f_or_coro, *args, **kwargs):
        r = f_or_coro(*args, **kwargs)
        try:
            r = await r
        except TypeError:
            # not a coroutine
            pass
        return r


redirect = Response.redirect
send_file = Response.send_file
