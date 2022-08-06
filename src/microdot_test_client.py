from io import BytesIO
import json
from microdot import Request


class TestResponse:
    """A response object issued by the Microdot test client."""
    def __init__(self, res):
        #: The numeric status code returned by the server.
        self.status_code = res.status_code
        #: The text reason associated with the status response, such as
        #: ``'OK'`` or ``'NOT FOUND'``.
        self.reason = res.reason
        #: A dictionary with the response headers.
        self.headers = res.headers
        #: The body of the response, as a bytes object.
        self.body = b''
        for body in res.body_iter():
            if isinstance(body, str):
                body = body.encode()
            self.body += body
        try:
            #: The body of the response, decoded to a UTF-8 string. Set to
            #: ``None`` if the response cannot be represented as UTF-8 text.
            self.text = self.body.decode()
        except ValueError:
            self.text = None
        #: The body of the JSON response, decoded to a dictionary or list. Set
        #: ``Note`` if the response does not have a JSON payload.
        self.json = None
        for name, value in self.headers.items():  # pragma: no branch
            if name.lower() == 'content-type':
                if value.lower() == 'application/json':
                    self.json = json.loads(self.text)
                break


class TestClient:
    """A test client for Microdot.

    :param app: The Microdot application instance.
    :param cookies: A dictionary of cookies to use when sending requests to the
                    application.

    The following example shows how to create a test client for an application
    and send a test request::

        from microdot import Microdot

        app = Microdot()

        @app.get('/')
        def index():
            return 'Hello, World!'

        def test_hello_world(self):
            client = TestClient(app)
            res = client.get('/')
            assert res.status_code == 200
            assert res.text == 'Hello, World!'
    """
    def __init__(self, app, cookies=None):
        self.app = app
        self.cookies = cookies or {}

    def request(self, method, path, headers=None, body=None):
        if headers is None:  # pragma: no branch
            headers = {}
        if body is None:
            body = b''
        elif isinstance(body, (dict, list)):
            body = json.dumps(body).encode()
            if 'Content-Type' not in headers and \
                    'content-type' not in headers:  # pragma: no cover
                headers['Content-Type'] = 'application/json'
        elif isinstance(body, str):
            body = body.encode()
        if body and 'Content-Length' not in headers and \
                'content-length' not in headers:
            headers['Content-Length'] = str(len(body))
        cookies = ''
        for name, value in self.cookies.items():
            if cookies:
                cookies += '; '
            cookies += name + '=' + value
        if cookies:
            if 'Cookie' in headers:
                headers['Cookie'] += '; ' + cookies
            else:
                headers['Cookie'] = cookies
        request_bytes = '{method} {path} HTTP/1.0\n'.format(
            method=method, path=path)
        if 'Host' not in headers:  # pragma: no branch
            headers['Host'] = 'example.com:1234'
        for header, value in headers.items():
            request_bytes += '{header}: {value}\n'.format(
                header=header, value=value)
        request_bytes = request_bytes.encode() + b'\n' + body

        req = Request.create(self.app, BytesIO(request_bytes),
                             ('127.0.0.1', 1234))
        res = self.app.dispatch_request(req)
        res.complete()

        for name, value in res.headers.items():
            if name.lower() == 'set-cookie':
                for cookie in value:
                    cookie_name, cookie_value = cookie.split('=', 1)
                    cookie_options = cookie_value.split(';')
                    delete = False
                    for option in cookie_options[1:]:
                        if option.strip().lower().startswith('expires='):
                            _, e = option.strip().split('=', 1)
                            # this is a very limited parser for cookie expiry
                            # that only detects a cookie deletion request when
                            # the date is 1/1/1970
                            if '1 jan 1970' in e.lower():  # pragma: no branch
                                delete = True
                                break
                    if delete:
                        if cookie_name in self.cookies:  # pragma: no branch
                            del self.cookies[cookie_name]
                    else:
                        self.cookies[cookie_name] = cookie_options[0]
        return TestResponse(res)

    def get(self, path, headers=None):
        """Send a GET request to the application.

        :param path: The request URL.
        :param headers: A dictionary of headers to send with the request.

        This method returns a
        :class:`TestResponse <microdot_test_client.TestResponse>` object.
        """
        return self.request('GET', path, headers=headers)

    def post(self, path, headers=None, body=None):
        """Send a POST request to the application.

        :param path: The request URL.
        :param headers: A dictionary of headers to send with the request.
        :param body: The request body. If a dictionary or list is provided,
                     a JSON-encoded body will be sent. A string body is encoded
                     to bytes as UTF-8. A bytes body is sent as-is.

        This method returns a
        :class:`TestResponse <microdot_test_client.TestResponse>` object.
        """
        return self.request('POST', path, headers=headers, body=body)

    def put(self, path, headers=None, body=None):
        """Send a PUT request to the application.

        :param path: The request URL.
        :param headers: A dictionary of headers to send with the request.
        :param body: The request body. If a dictionary or list is provided,
                     a JSON-encoded body will be sent. A string body is encoded
                     to bytes as UTF-8. A bytes body is sent as-is.

        This method returns a
        :class:`TestResponse <microdot_test_client.TestResponse>` object.
        """
        return self.request('PUT', path, headers=headers, body=body)

    def patch(self, path, headers=None, body=None):
        """Send a PATCH request to the application.

        :param path: The request URL.
        :param headers: A dictionary of headers to send with the request.
        :param body: The request body. If a dictionary or list is provided,
                     a JSON-encoded body will be sent. A string body is encoded
                     to bytes as UTF-8. A bytes body is sent as-is.

        This method returns a
        :class:`TestResponse <microdot_test_client.TestResponse>` object.
        """
        return self.request('PATCH', path, headers=headers, body=body)

    def delete(self, path, headers=None):
        """Send a DELETE request to the application.

        :param path: The request URL.
        :param headers: A dictionary of headers to send with the request.

        This method returns a
        :class:`TestResponse <microdot_test_client.TestResponse>` object.
        """
        return self.request('DELETE', path, headers=headers)
