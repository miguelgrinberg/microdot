"""
microdot_asyncio
----------------

The ``microdot_asyncio`` module defines a few classes that help implement
HTTP-based servers for MicroPython and standard Python that use ``asyncio``
and coroutines.
"""
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

try:
    import uio as io
except ImportError:
    import io

from microdot import Microdot as BaseMicrodot
from microdot import print_exception
from microdot import Request as BaseRequest
from microdot import Response as BaseResponse


def _iscoroutine(coro):
    return hasattr(coro, 'send') and hasattr(coro, 'throw')


class _AsyncBytesIO:
    def __init__(self, data):
        self.stream = io.BytesIO(data)

    async def read(self, n=-1):
        return self.stream.read(n)

    async def readline(self):  # pragma: no cover
        return self.stream.readline()

    async def readexactly(self, n):  # pragma: no cover
        return self.stream.read(n)

    async def readuntil(self, separator=b'\n'):  # pragma: no cover
        return self.stream.readuntil(separator=separator)


class Request(BaseRequest):
    @staticmethod
    async def create(app, client_stream, client_addr):
        """Create a request object.

        :param app: The Microdot application instance.
        :param client_stream: An input stream from where the request data can
                              be read.
        :param client_addr: The address of the client, as a tuple.

        This method is a coroutine. It returns a newly created ``Request``
        object.
        """
        # request line
        line = (await Request._safe_readline(client_stream)).strip().decode()
        if not line:  # pragma: no cover
            return None
        method, url, http_version = line.split()
        http_version = http_version.split('/', 1)[1]

        # headers
        headers = {}
        content_length = 0
        while True:
            line = (await Request._safe_readline(
                client_stream)).strip().decode()
            if line == '':
                break
            header, value = line.split(':', 1)
            value = value.strip()
            headers[header] = value
            if header.lower() == 'content-length':
                content_length = int(value)

        # body
        body = b''
        print(Request.max_body_length)
        if content_length and content_length <= Request.max_body_length:
            body = await client_stream.readexactly(content_length)
            stream = None
        else:
            body = b''
            stream = client_stream

        return Request(app, client_addr, method, url, http_version, headers,
                       body=body, stream=stream)

    @property
    def stream(self):
        if self._stream is None:
            self._stream = _AsyncBytesIO(self._body)
        return self._stream

    @staticmethod
    async def _safe_readline(stream):
        line = (await stream.readline())
        if len(line) > Request.max_readline:
            raise ValueError('line too long')
        return line


class Response(BaseResponse):
    """An HTTP response class.

    :param body: The body of the response. If a dictionary or list is given,
                 a JSON formatter is used to generate the body.
    :param status_code: The numeric HTTP status code of the response. The
                        default is 200.
    :param headers: A dictionary of headers to include in the response.
    :param reason: A custom reason phrase to add after the status code. The
                   default is "OK" for responses with a 200 status code and
                   "N/A" for any other status codes.
    """
    async def write(self, stream):
        self.complete()

        # status code
        reason = self.reason if self.reason is not None else \
            ('OK' if self.status_code == 200 else 'N/A')
        await stream.awrite('HTTP/1.0 {status_code} {reason}\r\n'.format(
            status_code=self.status_code, reason=reason).encode())

        # headers
        for header, value in self.headers.items():
            values = value if isinstance(value, list) else [value]
            for value in values:
                await stream.awrite('{header}: {value}\r\n'.format(
                    header=header, value=value).encode())
        await stream.awrite(b'\r\n')

        # body
        if self.body:
            if hasattr(self.body, 'read'):
                while True:
                    buf = self.body.read(self.send_file_buffer_size)
                    if len(buf):
                        await stream.awrite(buf)
                    if len(buf) < self.send_file_buffer_size:
                        break
                if hasattr(self.body, 'close'):  # pragma: no cover
                    self.body.close()
            else:
                await stream.awrite(self.body)


class Microdot(BaseMicrodot):
    async def start_server(self, host='0.0.0.0', port=5000, debug=False):
        """Start the Microdot web server as a coroutine. This coroutine does
        not normally return, as the server enters an endless listening loop.
        The :func:`shutdown` function provides a method for terminating the
        server gracefully.

        :param host: The hostname or IP address of the network interface that
                     will be listening for requests. A value of ``'0.0.0.0'``
                     (the default) indicates that the server should listen for
                     requests on all the available interfaces, and a value of
                     ``127.0.0.1`` indicates that the server should listen
                     for requests only on the internal networking interface of
                     the host.
        :param port: The port number to listen for requests. The default is
                     port 5000.
        :param debug: If ``True``, the server logs debugging information. The
                      default is ``False``.

        This method is a coroutine.

        Example::

            import asyncio
            from microdot_asyncio import Microdot

            app = Microdot()

            @app.route('/')
            async def index():
                return 'Hello, world!'

            async def main():
                await app.start_server(debug=True)

            asyncio.run(main())
        """
        self.debug = debug

        async def serve(reader, writer):
            if not hasattr(writer, 'awrite'):  # pragma: no cover
                # CPython provides the awrite and aclose methods in 3.8+
                async def awrite(self, data):
                    self.write(data)
                    await self.drain()

                async def aclose(self):
                    self.close()
                    await self.wait_closed()

                from types import MethodType
                writer.awrite = MethodType(awrite, writer)
                writer.aclose = MethodType(aclose, writer)

            await self.dispatch_request(reader, writer)

        if self.debug:  # pragma: no cover
            print('Starting async server on {host}:{port}...'.format(
                host=host, port=port))

        self.server = await asyncio.start_server(serve, host, port)
        while True:
            try:
                await self.server.wait_closed()
                break
            except AttributeError:  # pragma: no cover
                # the task hasn't been initialized in the server object yet
                # wait a bit and try again
                await asyncio.sleep(0.1)

    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Start the web server. This function does not normally return, as
        the server enters an endless listening loop. The :func:`shutdown`
        function provides a method for terminating the server gracefully.

        :param host: The hostname or IP address of the network interface that
                     will be listening for requests. A value of ``'0.0.0.0'``
                     (the default) indicates that the server should listen for
                     requests on all the available interfaces, and a value of
                     ``127.0.0.1`` indicates that the server should listen
                     for requests only on the internal networking interface of
                     the host.
        :param port: The port number to listen for requests. The default is
                     port 5000.
        :param debug: If ``True``, the server logs debugging information. The
                      default is ``False``.

        Example::

            from microdot_asyncio import Microdot

            app = Microdot()

            @app.route('/')
            async def index():
                return 'Hello, world!'

            app.run(debug=True)
        """
        asyncio.run(self.start_server(host=host, port=port, debug=debug))

    def shutdown(self):
        self.server.close()

    async def dispatch_request(self, reader, writer):
        req = None
        try:
            req = await Request.create(self, reader,
                                       writer.get_extra_info('peername'))
        except Exception as exc:  # pragma: no cover
            print_exception(exc)
        if req:
            if req.content_length > req.max_content_length:
                if 413 in self.error_handlers:
                    res = await self._invoke_handler(
                        self.error_handlers[413], req)
                else:
                    res = 'Payload too large', 413
            else:
                f = self.find_route(req)
                try:
                    res = None
                    if f:
                        for handler in self.before_request_handlers:
                            res = await self._invoke_handler(handler, req)
                            if res:
                                break
                        if res is None:
                            res = await self._invoke_handler(
                                f, req, **req.url_args)
                        if isinstance(res, tuple):
                            res = Response(*res)
                        elif not isinstance(res, Response):
                            res = Response(res)
                        for handler in self.after_request_handlers:
                            res = await self._invoke_handler(
                                handler, req, res) or res
                    elif 404 in self.error_handlers:
                        res = await self._invoke_handler(
                            self.error_handlers[404], req)
                    else:
                        res = 'Not found', 404
                except Exception as exc:
                    print_exception(exc)
                    res = None
                    if exc.__class__ in self.error_handlers:
                        try:
                            res = await self._invoke_handler(
                                self.error_handlers[exc.__class__], req, exc)
                        except Exception as exc2:  # pragma: no cover
                            print_exception(exc2)
                    if res is None:
                        if 500 in self.error_handlers:
                            res = await self._invoke_handler(
                                self.error_handlers[500], req)
                        else:
                            res = 'Internal server error', 500
        else:
            res = 'Bad request', 400
        if isinstance(res, tuple):
            res = Response(*res)
        elif not isinstance(res, Response):
            res = Response(res)
        await res.write(writer)
        await writer.aclose()
        if self.debug and req:  # pragma: no cover
            print('{method} {path} {status_code}'.format(
                method=req.method, path=req.path,
                status_code=res.status_code))

    async def _invoke_handler(self, f_or_coro, *args, **kwargs):
        ret = f_or_coro(*args, **kwargs)
        if _iscoroutine(ret):
            ret = await ret
        return ret


redirect = Response.redirect
send_file = Response.send_file
