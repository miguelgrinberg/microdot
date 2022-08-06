from microdot_asyncio import Request, _AsyncBytesIO
from microdot_test_client import TestClient as BaseTestClient, \
    TestResponse as BaseTestResponse


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
        async for body in res.body_iter():
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
    async def request(self, method, path, headers=None, body=None):
        headers = headers or {}
        body, headers = self._process_body(body, headers)
        cookies, headers = self._process_cookies(headers)
        request_bytes = self._render_request(method, path, headers, body)

        req = await Request.create(self.app, _AsyncBytesIO(request_bytes),
                                   ('127.0.0.1', 1234))
        res = await self.app.dispatch_request(req)
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
