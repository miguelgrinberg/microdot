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
from microdot import mro
from microdot import NoCaseDict
from microdot import Request as BaseRequest
from microdot import Response as BaseResponse
from microdot import print_exception
from microdot import HTTPException
from microdot import MUTED_SOCKET_ERRORS


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

    async def awrite(self, data):  # pragma: no cover
        return self.stream.write(data)

    async def aclose(self):  # pragma: no cover
        pass


class Request(BaseRequest):
    @staticmethod
    async def create(app, client_reader, client_writer, client_addr):
        """Create a request object.

        :param app: The Microdot application instance.
        :param client_reader: An input stream from where the request data can
                              be read.
        :param client_writer: An output stream where the response data can be
                              written.
        :param client_addr: The address of the client, as a tuple.

        This method is a coroutine. It returns a newly created ``Request``
        object.
        """
        # request line
        line = (await Request._safe_readline(client_reader)).strip().decode()
        if not line:
            return None
        method, url, http_version = line.split()
        http_version = http_version.split('/', 1)[1]

        # headers
        headers = NoCaseDict()
        content_length = 0
        while True:
            line = (await Request._safe_readline(
                client_reader)).strip().decode()
            if line == '':
                break
            header, value = line.split(':', 1)
            value = value.strip()
            headers[header] = value
            if header.lower() == 'content-length':
                content_length = int(value)

        # body
        body = b''
        if content_length and content_length <= Request.max_body_length:
            body = await client_reader.readexactly(content_length)
            stream = None
        else:
            body = b''
            stream = client_reader

        return Request(app, client_addr, method, url, http_version, headers,
                       body=body, stream=stream,
                       sock=(client_reader, client_writer))

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
                 a JSON formatter is used to generate the body. If a file-like
                 object or an async generator is given, a streaming response is
                 used. If a string is given, it is encoded from UTF-8. Else,
                 the body should be a byte sequence.
    :param status_code: The numeric HTTP status code of the response. The
                        default is 200.
    :param headers: A dictionary of headers to include in the response.
    :param reason: A custom reason phrase to add after the status code. The
                   default is "OK" for responses with a 200 status code and
                   "N/A" for any other status codes.
    """

    async def write(self, stream):
        self.complete()

        try:
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
            async for body in self.body_iter():
                if isinstance(body, str):  # pragma: no cover
                    body = body.encode()
                await stream.awrite(body)
        except OSError as exc:  # pragma: no cover
            if exc.errno in MUTED_SOCKET_ERRORS or \
                    exc.args[0] == 'Connection lost':
                pass
            else:
                raise

    def body_iter(self):
        if hasattr(self.body, '__anext__'):
            # response body is an async generator
            return self.body

        response = self

        class iter:
            def __aiter__(self):
                if response.body:
                    self.i = 0  # need to determine type of response.body
                else:
                    self.i = -1  # no response body
                return self

            async def __anext__(self):
                if self.i == -1:
                    raise StopAsyncIteration
                if self.i == 0:
                    if hasattr(response.body, 'read'):
                        self.i = 2  # response body is a file-like object
                    elif hasattr(response.body, '__next__'):
                        self.i = 1  # response body is a sync generator
                        return next(response.body)
                    else:
                        self.i = -1  # response body is a plain string
                        return response.body
                elif self.i == 1:
                    try:
                        return next(response.body)
                    except StopIteration:
                        raise StopAsyncIteration
                buf = response.body.read(response.send_file_buffer_size)
                if _iscoroutine(buf):  # pragma: no cover
                    buf = await buf
                if len(buf) < response.send_file_buffer_size:
                    self.i = -1
                    if hasattr(response.body, 'close'):  # pragma: no cover
                        result = response.body.close()
                        if _iscoroutine(result):
                            await result
                return buf

        return iter()


class Microdot(BaseMicrodot):
    async def start_server(self, host='0.0.0.0', port=5000, debug=False,
                           ssl=None):
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
        :param ssl: An ``SSLContext`` instance or ``None`` if the server should
                    not use TLS. The default is ``None``.

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

            await self.handle_request(reader, writer)

        if self.debug:  # pragma: no cover
            print('Starting async server on {host}:{port}...'.format(
                host=host, port=port))

        try:
            self.server = await asyncio.start_server(serve, host, port,
                                                     ssl=ssl)
        except TypeError:
            self.server = await asyncio.start_server(serve, host, port)

        while True:
            try:
                await self.server.wait_closed()
                break
            except AttributeError:  # pragma: no cover
                # the task hasn't been initialized in the server object yet
                # wait a bit and try again
                await asyncio.sleep(0.1)

    def run(self, host='0.0.0.0', port=5000, debug=False, ssl=None):
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
        :param ssl: An ``SSLContext`` instance or ``None`` if the server should
                    not use TLS. The default is ``None``.

        Example::

            from microdot_asyncio import Microdot

            app = Microdot()

            @app.route('/')
            async def index():
                return 'Hello, world!'

            app.run(debug=True)
        """
        asyncio.run(self.start_server(host=host, port=port, debug=debug,
                                      ssl=ssl))

    def shutdown(self):
        self.server.close()

    async def handle_request(self, reader, writer):
        req = None
        try:
            req = await Request.create(self, reader, writer,
                                       writer.get_extra_info('peername'))
        except Exception as exc:  # pragma: no cover
            print_exception(exc)

        res = await self.dispatch_request(req)
        if res != Response.already_handled:  # pragma: no branch
            await res.write(writer)
        try:
            await writer.aclose()
        except OSError as exc:  # pragma: no cover
            if exc.errno in MUTED_SOCKET_ERRORS:
                pass
            else:
                raise
        if self.debug and req:  # pragma: no cover
            print('{method} {path} {status_code}'.format(
                method=req.method, path=req.path,
                status_code=res.status_code))

    async def dispatch_request(self, req):
        after_request_handled = False
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
                    if callable(f):
                        for handler in self.before_request_handlers:
                            res = await self._invoke_handler(handler, req)
                            if res:
                                break
                        if res is None:
                            res = await self._invoke_handler(
                                f, req, **req.url_args)
                        if isinstance(res, tuple):
                            body = res[0]
                            if isinstance(res[1], int):
                                status_code = res[1]
                                headers = res[2] if len(res) > 2 else {}
                            else:
                                status_code = 200
                                headers = res[1]
                            res = Response(body, status_code, headers)
                        elif not isinstance(res, Response):
                            res = Response(res)
                        for handler in self.after_request_handlers:
                            res = await self._invoke_handler(
                                handler, req, res) or res
                        for handler in req.after_request_handlers:
                            res = await self._invoke_handler(
                                handler, req, res) or res
                        after_request_handled = True
                    elif f in self.error_handlers:
                        res = await self._invoke_handler(
                            self.error_handlers[f], req)
                    else:
                        res = 'Not found', f
                except HTTPException as exc:
                    if exc.status_code in self.error_handlers:
                        res = self.error_handlers[exc.status_code](req)
                    else:
                        res = exc.reason, exc.status_code
                except Exception as exc:
                    print_exception(exc)
                    exc_class = None
                    res = None
                    if exc.__class__ in self.error_handlers:
                        exc_class = exc.__class__
                    else:
                        for c in mro(exc.__class__)[1:]:
                            if c in self.error_handlers:
                                exc_class = c
                                break
                    if exc_class:
                        try:
                            res = await self._invoke_handler(
                                self.error_handlers[exc_class], req, exc)
                        except Exception as exc2:  # pragma: no cover
                            print_exception(exc2)
                    if res is None:
                        if 500 in self.error_handlers:
                            res = await self._invoke_handler(
                                self.error_handlers[500], req)
                        else:
                            res = 'Internal server error', 500
        else:
            if 400 in self.error_handlers:
                res = await self._invoke_handler(self.error_handlers[400], req)
            else:
                res = 'Bad request', 400
        if isinstance(res, tuple):
            res = Response(*res)
        elif not isinstance(res, Response):
            res = Response(res)
        if not after_request_handled:
            for handler in self.after_error_request_handlers:
                res = await self._invoke_handler(
                    handler, req, res) or res
        return res

    async def _invoke_handler(self, f_or_coro, *args, **kwargs):
        ret = f_or_coro(*args, **kwargs)
        if _iscoroutine(ret):
            ret = await ret
        return ret


abort = Microdot.abort
Response.already_handled = Response()
redirect = Response.redirect
send_file = Response.send_file
