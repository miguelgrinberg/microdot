from microdot_asyncio import Request, Response, _AsyncBytesIO
from microdot_test_client import TestClient as BaseTestClient, \
    TestResponse as BaseTestResponse
try:
    from microdot_asyncio_websocket import WebSocket
except:  # pragma: no cover  # noqa: E722
    WebSocket = None


class TestResponse(BaseTestResponse):
    """A response object issued by the Microdot test client."""

    @classmethod
    async def create(cls, res):
        test_res = cls()
        test_res._initialize_response(res)
        await test_res._initialize_body(res)
        test_res._process_text_body()
        test_res._process_json_body()
        return test_res

    async def _initialize_body(self, res):
        self.body = b''
        async for body in res.body_iter():  # pragma: no branch
            if isinstance(body, str):
                body = body.encode()
            self.body += body


class TestClient(BaseTestClient):
    """A test client for Microdot's Asynchronous web server.

    :param app: The Microdot application instance.
    :param cookies: A dictionary of cookies to use when sending requests to the
                    application.

    The following example shows how to create a test client for an application
    and send a test request::

        from microdot_asyncio import Microdot

        app = Microdot()

        @app.get('/')
        async def index():
            return 'Hello, World!'

        async def test_hello_world(self):
            client = TestClient(app)
            res = await client.get('/')
            assert res.status_code == 200
            assert res.text == 'Hello, World!'
    """
    async def request(self, method, path, headers=None, body=None, sock=None):
        headers = headers or {}
        body, headers = self._process_body(body, headers)
        cookies, headers = self._process_cookies(headers)
        request_bytes = self._render_request(method, path, headers, body)
        if sock:
            reader = sock[0]
            reader.buffer = request_bytes
            writer = sock[1]
        else:
            reader = _AsyncBytesIO(request_bytes)
            writer = _AsyncBytesIO(b'')

        req = await Request.create(self.app, reader, writer,
                                   ('127.0.0.1', 1234))
        res = await self.app.dispatch_request(req)
        if res == Response.already_handled:
            return None
        res.complete()

        self._update_cookies(res)
        return await TestResponse.create(res)

    async def get(self, path, headers=None):
        """Send a GET request to the application.

        :param path: The request URL.
        :param headers: A dictionary of headers to send with the request.

        This method returns a
        :class:`TestResponse <microdot_test_client.TestResponse>` object.
        """
        return await self.request('GET', path, headers=headers)

    async def post(self, path, headers=None, body=None):
        """Send a POST request to the application.

        :param path: The request URL.
        :param headers: A dictionary of headers to send with the request.
        :param body: The request body. If a dictionary or list is provided,
                     a JSON-encoded body will be sent. A string body is encoded
                     to bytes as UTF-8. A bytes body is sent as-is.

        This method returns a
        :class:`TestResponse <microdot_test_client.TestResponse>` object.
        """
        return await self.request('POST', path, headers=headers, body=body)

    async def put(self, path, headers=None, body=None):
        """Send a PUT request to the application.

        :param path: The request URL.
        :param headers: A dictionary of headers to send with the request.
        :param body: The request body. If a dictionary or list is provided,
                     a JSON-encoded body will be sent. A string body is encoded
                     to bytes as UTF-8. A bytes body is sent as-is.

        This method returns a
        :class:`TestResponse <microdot_test_client.TestResponse>` object.
        """
        return await self.request('PUT', path, headers=headers, body=body)

    async def patch(self, path, headers=None, body=None):
        """Send a PATCH request to the application.

        :param path: The request URL.
        :param headers: A dictionary of headers to send with the request.
        :param body: The request body. If a dictionary or list is provided,
                     a JSON-encoded body will be sent. A string body is encoded
                     to bytes as UTF-8. A bytes body is sent as-is.

        This method returns a
        :class:`TestResponse <microdot_test_client.TestResponse>` object.
        """
        return await self.request('PATCH', path, headers=headers, body=body)

    async def delete(self, path, headers=None):
        """Send a DELETE request to the application.

        :param path: The request URL.
        :param headers: A dictionary of headers to send with the request.

        This method returns a
        :class:`TestResponse <microdot_test_client.TestResponse>` object.
        """
        return await self.request('DELETE', path, headers=headers)

    async def websocket(self, path, client, headers=None):
        """Send a websocket connection request to the application.

        :param path: The request URL.
        :param client: A generator function that yields client messages.
        :param headers: A dictionary of headers to send with the request.
        """
        gen = client()

        class FakeWebSocket:
            def __init__(self):
                self.started = False
                self.closed = False
                self.buffer = b''

            async def _next(self, data=None):
                try:
                    data = (await gen.asend(data)) if hasattr(gen, 'asend') \
                        else gen.send(data)
                except (StopIteration, StopAsyncIteration):
                    if not self.closed:
                        self.closed = True
                        raise OSError(32, 'Websocket connection closed')
                    return  # pragma: no cover
                opcode = WebSocket.TEXT if isinstance(data, str) \
                    else WebSocket.BINARY
                return WebSocket._encode_websocket_frame(opcode, data)

            async def read(self, n):
                if not self.buffer:
                    self.started = True
                    self.buffer = await self._next()
                data = self.buffer[:n]
                self.buffer = self.buffer[n:]
                return data

            async def readexactly(self, n):  # pragma: no cover
                return await self.read(n)

            async def readline(self):
                line = b''
                while True:
                    line += await self.read(1)
                    if line[-1] in [b'\n', 10]:
                        break
                return line

            async def awrite(self, data):
                if self.started:
                    h = WebSocket._parse_frame_header(data[0:2])
                    if h[3] < 0:
                        data = data[2 - h[3]:]
                    else:
                        data = data[2:]
                    if h[1] == WebSocket.TEXT:
                        data = data.decode()
                    self.buffer = await self._next(data)

        ws_headers = {
            'Upgrade': 'websocket',
            'Connection': 'Upgrade',
            'Sec-WebSocket-Version': '13',
            'Sec-WebSocket-Key': 'dGhlIHNhbXBsZSBub25jZQ==',
        }
        ws_headers.update(headers or {})
        sock = FakeWebSocket()
        return await self.request('GET', path, headers=ws_headers,
                                  sock=(sock, sock))
