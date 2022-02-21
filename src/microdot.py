"""
microdot
--------

The ``microdot`` module defines a few classes that help implement HTTP-based
servers for MicroPython and standard Python, with multithreading support for
Python interpreters that support it.
"""
try:
    from sys import print_exception
except ImportError:  # pragma: no cover
    import traceback

    def print_exception(exc):
        traceback.print_exc()
try:
    import uerrno as errno
except ImportError:
    import errno

concurrency_mode = 'threaded'

try:  # pragma: no cover
    import threading

    def create_thread(f, *args, **kwargs):
        # use the threading module
        threading.Thread(target=f, args=args, kwargs=kwargs).start()
except ImportError:  # pragma: no cover
    try:
        import _thread

        def create_thread(f, *args, **kwargs):
            # use MicroPython's _thread module
            def run():
                f(*args, **kwargs)

            _thread.start_new_thread(run, ())
    except ImportError:
        def create_thread(f, *args, **kwargs):
            # no threads available, call function synchronously
            f(*args, **kwargs)

        concurrency_mode = 'sync'
try:
    import ujson as json
except ImportError:
    import json

try:
    import ure as re
except ImportError:
    import re

try:
    import usocket as socket
except ImportError:
    try:
        import socket
    except ImportError:  # pragma: no cover
        socket = None


def urldecode(string):
    string = string.replace('+', ' ')
    parts = string.split('%')
    if len(parts) == 1:
        return string
    result = [parts[0]]
    for item in parts[1:]:
        if item == '':
            result.append('%')
        else:
            code = item[:2]
            result.append(chr(int(code, 16)))
            result.append(item[2:])
    return ''.join(result)


class MultiDict(dict):
    """A subclass of dictionary that can hold multiple values for the same
    key. It is used to hold key/value pairs decoded from query strings and
    form submissions.

    :param initial_dict: an initial dictionary of key/value pairs to
                         initialize this object with.

    Example::

        >>> d = MultiDict()
        >>> d['sort'] = 'name'
        >>> d['sort'] = 'email'
        >>> print(d['sort'])
        'name'
        >>> print(d.getlist('sort'))
        ['name', 'email']
    """
    def __init__(self, initial_dict=None):
        super().__init__()
        if initial_dict:
            for key, value in initial_dict.items():
                self[key] = value

    def __setitem__(self, key, value):
        if key not in self:
            super().__setitem__(key, [])
        super().__getitem__(key).append(value)

    def __getitem__(self, key):
        return super().__getitem__(key)[0]

    def get(self, key, default=None, type=None):
        """Return the value for a given key.

        :param key: The key to retrieve.
        :param default: A default value to use if the key does not exist.
        :param type: A type conversion callable to apply to the value.

        If the multidict contains more than one value for the requested key,
        this method returns the first value only.

        Example::

            >>> d = MultiDict()
            >>> d['age'] = '42'
            >>> d.get('age')
            '42'
            >>> d.get('age', type=int)
            42
            >>> d.get('name', default='noname')
            'noname'
        """
        if key not in self:
            return default
        value = self[key]
        if type is not None:
            value = type(value)
        return value

    def getlist(self, key, type=None):
        """Return all the values for a given key.

        :param key: The key to retrieve.
        :param type: A type conversion callable to apply to the values.

        If the requested key does not exist in the dictionary, this method
        returns an empty list.

        Example::

            >>> d = MultiDict()
            >>> d.getlist('items')
            []
            >>> d['items'] = '3'
            >>> d.getlist('items')
            ['3']
            >>> d['items'] = '56'
            >>> d.getlist('items')
            ['3', '56']
            >>> d.getlist('items', type=int)
            [3, 56]
        """
        if key not in self:
            return []
        values = super().__getitem__(key)
        if type is not None:
            values = [type(value) for value in values]
        return values


class Request():
    """An HTTP request class.

    :var app: The application instance to which this request belongs.
    :var client_addr: The address of the client, as a tuple (host, port).
    :var method: The HTTP method of the request.
    :var path: The path portion of the URL.
    :var query_string: The query string portion of the URL.
    :var args: The parsed query string, as a :class:`MultiDict` object.
    :var headers: A dictionary with the headers included in the request.
    :var cookies: A dictionary with the cookies included in the request.
    :var content_length: The parsed ``Content-Length`` header.
    :var content_type: The parsed ``Content-Type`` header.
    :var stream: The input stream, containing the request body.
    :var body: The body of the request, as bytes.
    :var json: The parsed JSON body, as a dictionary or list, or ``None`` if
               the request does not have a JSON body.
    :var form: The parsed form submission body, as a :class:`MultiDict` object,
               or ``None`` if the request does not have a form submission.
    :var g: A general purpose container for applications to store data during
            the life of the request.
    """
    #: Specify the maximum payload size that is accepted. Requests with larger
    #: payloads will be rejected with a 413 status code. Applications can
    #: change this maximum as necessary.
    #:
    #: Example::
    #:
    #:    Request.max_content_length = 1 * 1024 * 1024  # 1MB requests allowed
    max_content_length = 16 * 1024

    #: Specify the maximum payload size that can be stored in ``body``.
    #: Requests with payloads that are larger than this size and up to
    #: ``max_content_length`` bytes will be accepted, but the application will
    #: only be able to access the body of the request by reading from
    #: ``stream``. Set to 0 if you always access the body as a stream.
    #:
    #: Example::
    #:
    #:    Request.max_body_length = 4 * 1024  # up to 4KB bodies read
    max_body_length = 16 * 1024

    #: Specify the maximum length allowed for a line in the request. Requests
    #: with longer lines will not be correctly interpreted. Applications can
    #: change this maximum as necessary.
    #:
    #: Example::
    #:
    #:    Request.max_readline = 16 * 1024  # 16KB lines allowed
    max_readline = 2 * 1024

    class G:
        pass

    def __init__(self, app, client_addr, method, url, http_version, headers,
                 body=None, stream=None):
        self.app = app
        self.client_addr = client_addr
        self.method = method
        self.path = url
        self.http_version = http_version
        if '?' in self.path:
            self.path, self.query_string = self.path.split('?', 1)
            self.args = self._parse_urlencoded(self.query_string)
        else:
            self.query_string = None
            self.args = {}
        self.headers = headers
        self.cookies = {}
        self.content_length = 0
        self.content_type = None
        for header, value in self.headers.items():
            header = header.lower()
            if header == 'content-length':
                self.content_length = int(value)
            elif header == 'content-type':
                self.content_type = value
            elif header == 'cookie':
                for cookie in value.split(';'):
                    name, value = cookie.strip().split('=', 1)
                    self.cookies[name] = value
        self._body = body
        self.body_used = False
        self._stream = stream
        self.stream_used = False
        self._json = None
        self._form = None
        self.g = Request.G()

    @staticmethod
    def create(app, client_stream, client_addr):
        """Create a request object.

        :param app: The Microdot application instance.
        :param client_stream: An input stream from where the request data can
                              be read.
        :param client_addr: The address of the client, as a tuple.

        This method returns a newly created ``Request`` object.
        """
        # request line
        line = Request._safe_readline(client_stream).strip().decode()
        if not line:
            return None
        method, url, http_version = line.split()
        http_version = http_version.split('/', 1)[1]

        # headers
        headers = {}
        while True:
            line = Request._safe_readline(client_stream).strip().decode()
            if line == '':
                break
            header, value = line.split(':', 1)
            value = value.strip()
            headers[header] = value

        return Request(app, client_addr, method, url, http_version, headers,
                       stream=client_stream)

    def _parse_urlencoded(self, urlencoded):
        data = MultiDict()
        for k, v in [pair.split('=', 1) for pair in urlencoded.split('&')]:
            data[urldecode(k)] = urldecode(v)
        return data

    @property
    def body(self):
        if self.stream_used:
            raise RuntimeError('Cannot use both stream and body')
        if self._body is None:
            self._body = b''
            if self.content_length and \
                    self.content_length <= Request.max_body_length:
                while len(self._body) < self.content_length:
                    data = self._stream.read(
                        self.content_length - len(self._body))
                    if len(data) == 0:  # pragma: no cover
                        raise EOFError()
                    self._body += data
                self.body_used = True
        return self._body

    @property
    def stream(self):
        if self.body_used:
            raise RuntimeError('Cannot use both stream and body')
        self.stream_used = True
        return self._stream

    @property
    def json(self):
        if self._json is None:
            if self.content_type is None:
                return None
            mime_type = self.content_type.split(';')[0]
            if mime_type != 'application/json':
                return None
            self._json = json.loads(self.body.decode())
        return self._json

    @property
    def form(self):
        if self._form is None:
            if self.content_type is None:
                return None
            mime_type = self.content_type.split(';')[0]
            if mime_type != 'application/x-www-form-urlencoded':
                return None
            self._form = self._parse_urlencoded(self.body.decode())
        return self._form

    @staticmethod
    def _safe_readline(stream):
        line = stream.readline(Request.max_readline + 1)
        if len(line) > Request.max_readline:
            raise ValueError('line too long')
        return line


class Response():
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
    types_map = {
        'css': 'text/css',
        'gif': 'image/gif',
        'html': 'text/html',
        'jpg': 'image/jpeg',
        'js': 'application/javascript',
        'json': 'application/json',
        'png': 'image/png',
        'txt': 'text/plain',
    }
    send_file_buffer_size = 1024

    def __init__(self, body='', status_code=200, headers=None, reason=None):
        self.status_code = status_code
        self.headers = headers.copy() if headers else {}
        self.reason = reason
        if isinstance(body, (dict, list)):
            self.body = json.dumps(body).encode()
            self.headers['Content-Type'] = 'application/json'
        elif isinstance(body, str):
            self.body = body.encode()
        else:
            # this applies to bytes or file-like objects
            self.body = body

    def set_cookie(self, cookie, value, path=None, domain=None, expires=None,
                   max_age=None, secure=False, http_only=False):
        """Add a cookie to the response.

        :param cookie: The cookie's name.
        :param value: The cookie's value.
        :param path: The cookie's path.
        :param domain: The cookie's domain.
        :param expires: The cookie expiration time, as a ``datetime`` object.
        :param max_age: The cookie's ``Max-Age`` value.
        :param secure: The cookie's ``secure`` flag.
        :param http_only: The cookie's ``HttpOnly`` flag.
        """
        http_cookie = '{cookie}={value}'.format(cookie=cookie, value=value)
        if path:
            http_cookie += '; Path=' + path
        if domain:
            http_cookie += '; Domain=' + domain
        if expires:
            http_cookie += '; Expires=' + expires.strftime(
                "%a, %d %b %Y %H:%M:%S GMT")
        if max_age:
            http_cookie += '; Max-Age=' + str(max_age)
        if secure:
            http_cookie += '; Secure'
        if http_only:
            http_cookie += '; HttpOnly'
        if 'Set-Cookie' in self.headers:
            self.headers['Set-Cookie'].append(http_cookie)
        else:
            self.headers['Set-Cookie'] = [http_cookie]

    def complete(self):
        if isinstance(self.body, bytes) and \
                'Content-Length' not in self.headers:
            self.headers['Content-Length'] = str(len(self.body))
        if 'Content-Type' not in self.headers:
            self.headers['Content-Type'] = 'text/plain'

    def write(self, stream):
        self.complete()

        # status code
        reason = self.reason if self.reason is not None else \
            ('OK' if self.status_code == 200 else 'N/A')
        stream.write('HTTP/1.0 {status_code} {reason}\r\n'.format(
            status_code=self.status_code, reason=reason).encode())

        # headers
        for header, value in self.headers.items():
            values = value if isinstance(value, list) else [value]
            for value in values:
                stream.write('{header}: {value}\r\n'.format(
                    header=header, value=value).encode())
        stream.write(b'\r\n')

        # body
        if self.body:
            if hasattr(self.body, 'read'):
                while True:
                    buf = self.body.read(self.send_file_buffer_size)
                    if len(buf):
                        stream.write(buf)
                    if len(buf) < self.send_file_buffer_size:
                        break
                if hasattr(self.body, 'close'):  # pragma: no cover
                    self.body.close()
            else:
                stream.write(self.body)

    @classmethod
    def redirect(cls, location, status_code=302):
        """Return a redirect response.

        :param location: The URL to redirect to.
        :param status_code: The 3xx status code to use for the redirect. The
                            default is 302.
        """
        if '\x0d' in location or '\x0a' in location:
            raise ValueError('invalid redirect URL')
        return cls(status_code=status_code, headers={'Location': location})

    @classmethod
    def send_file(cls, filename, status_code=200, content_type=None):
        """Send file contents in a response.

        :param filename: The filename of the file.
        :param status_code: The 3xx status code to use for the redirect. The
                            default is 302.
        :param content_type: The ``Content-Type`` header to use in the
                             response. If omitted, it is generated
                             automatically from the file extension.

        Security note: The filename is assumed to be trusted. Never pass
        filenames provided by the user before validating and sanitizing them
        first.
        """
        if content_type is None:
            ext = filename.split('.')[-1]
            if ext in Response.types_map:
                content_type = Response.types_map[ext]
            else:
                content_type = 'application/octet-stream'
        f = open(filename, 'rb')
        return cls(body=f, status_code=status_code,
                   headers={'Content-Type': content_type})


class URLPattern():
    def __init__(self, url_pattern):
        self.pattern = ''
        self.args = []
        use_regex = False
        for segment in url_pattern.lstrip('/').split('/'):
            if segment and segment[0] == '<':
                if segment[-1] != '>':
                    raise ValueError('invalid URL pattern')
                segment = segment[1:-1]
                if ':' in segment:
                    type_, name = segment.rsplit(':', 1)
                else:
                    type_ = 'string'
                    name = segment
                if type_ == 'string':
                    pattern = '[^/]+'
                elif type_ == 'int':
                    pattern = '\\d+'
                elif type_ == 'path':
                    pattern = '.+'
                elif type_.startswith('re:'):
                    pattern = type_[3:]
                else:
                    raise ValueError('invalid URL segment type')
                use_regex = True
                self.pattern += '/({pattern})'.format(pattern=pattern)
                self.args.append({'type': type_, 'name': name})
            else:
                self.pattern += '/{segment}'.format(segment=segment)
        if use_regex:
            self.pattern = re.compile('^' + self.pattern + '$')

    def match(self, path):
        if isinstance(self.pattern, str):
            if path != self.pattern:
                return
            return {}
        g = self.pattern.match(path)
        if not g:
            return
        args = {}
        i = 1
        for arg in self.args:
            value = g.group(i)
            if arg['type'] == 'int':
                value = int(value)
            args[arg['name']] = value
            i += 1
        return args


class Microdot():
    """An HTTP application class.

    This class implements an HTTP application instance and is heavily
    influenced by the ``Flask`` class of the Flask framework. It is typically
    declared near the start of the main application script.

    Example::

        from microdot import Microdot

        app = Microdot()
    """

    def __init__(self):
        self.url_map = []
        self.before_request_handlers = []
        self.after_request_handlers = []
        self.error_handlers = {}
        self.shutdown_requested = False
        self.debug = False
        self.server = None

    def route(self, url_pattern, methods=None):
        """Decorator that is used to register a function as a request handler
        for a given URL.

        :param url_pattern: The URL pattern that will be compared against
                            incoming requests.
        :param methods: The list of HTTP methods to be handled by the
                        decorated function. If omitted, only ``GET`` requests
                        are handled.

        The URL pattern can be a static path (for example, ``/users`` or
        ``/api/invoices/search``) or a path with dynamic components enclosed
        in ``<`` and ``>`` (for example, ``/users/<id>`` or
        ``/invoices/<number>/products``). Dynamic path components can also
        include a type prefix, separated from the name with a colon (for
        example, ``/users/<int:id>``). The type can be ``string`` (the
        default), ``int``, ``path`` or ``re:[regular-expression]``.

        The first argument of the decorated function must be
        the request object. Any path arguments that are specified in the URL
        pattern are passed as keyword arguments. The return value of the
        function must be a :class:`Response` instance, or the arguments to
        be passed to this class.

        Example::

            @app.route('/')
            def index(request):
                return 'Hello, world!'
        """
        def decorated(f):
            self.url_map.append(
                (methods or ['GET'], URLPattern(url_pattern), f))
            return f
        return decorated

    def get(self, url_pattern):
        """Decorator that is used to register a function as a ``GET`` request
        handler for a given URL.

        :param url_pattern: The URL pattern that will be compared against
                            incoming requests.

        This decorator can be used as an alias to the ``route`` decorator with
        ``methods=['GET']``.

        Example::

            @app.get('/users/<int:id>')
            def get_user(request, id):
                # ...
        """
        return self.route(url_pattern, methods=['GET'])

    def post(self, url_pattern):
        """Decorator that is used to register a function as a ``POST`` request
        handler for a given URL.

        :param url_pattern: The URL pattern that will be compared against
                            incoming requests.

        This decorator can be used as an alias to the``route`` decorator with
        ``methods=['POST']``.

        Example::

            @app.post('/users')
            def create_user(request):
                # ...
        """
        return self.route(url_pattern, methods=['POST'])

    def put(self, url_pattern):
        """Decorator that is used to register a function as a ``PUT`` request
        handler for a given URL.

        :param url_pattern: The URL pattern that will be compared against
                            incoming requests.

        This decorator can be used as an alias to the ``route`` decorator with
        ``methods=['PUT']``.

        Example::

            @app.put('/users/<int:id>')
            def edit_user(request, id):
                # ...
        """
        return self.route(url_pattern, methods=['PUT'])

    def patch(self, url_pattern):
        """Decorator that is used to register a function as a ``PATCH`` request
        handler for a given URL.

        :param url_pattern: The URL pattern that will be compared against
                            incoming requests.

        This decorator can be used as an alias to the ``route`` decorator with
        ``methods=['PATCH']``.

        Example::

            @app.patch('/users/<int:id>')
            def edit_user(request, id):
                # ...
        """
        return self.route(url_pattern, methods=['PATCH'])

    def delete(self, url_pattern):
        """Decorator that is used to register a function as a ``DELETE``
        request handler for a given URL.

        :param url_pattern: The URL pattern that will be compared against
                            incoming requests.

        This decorator can be used as an alias to the ``route`` decorator with
        ``methods=['DELETE']``.

        Example::

            @app.delete('/users/<int:id>')
            def delete_user(request, id):
                # ...
        """
        return self.route(url_pattern, methods=['DELETE'])

    def before_request(self, f):
        """Decorator to register a function to run before each request is
        handled. The decorated function must take a single argument, the
        request object.

        Example::

            @app.before_request
            def func(request):
                # ...
        """
        self.before_request_handlers.append(f)
        return f

    def after_request(self, f):
        """Decorator to register a function to run after each request is
        handled. The decorated function must take two arguments, the request
        and response objects. The return value of the function must be an
        updated response object.

        Example::

            @app.before_request
            def func(request, response):
                # ...
        """
        self.after_request_handlers.append(f)
        return f

    def errorhandler(self, status_code_or_exception_class):
        """Decorator to register a function as an error handler. Error handler
        functions for numeric HTTP status codes must accept a single argument,
        the request object. Error handler functions for Python exceptions
        must accept two arguments, the request object and the exception
        object.

        :param status_code_or_exception_class: The numeric HTTP status code or
                                               Python exception class to
                                               handle.

        Examples::

            @app.errorhandler(404)
            def not_found(request):
                return 'Not found'

            @app.errorhandler(RuntimeError)
            def runtime_error(request, exception):
                return 'Runtime error'
        """
        def decorated(f):
            self.error_handlers[status_code_or_exception_class] = f
            return f
        return decorated

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

            from microdot import Microdot

            app = Microdot()

            @app.route('/')
            def index():
                return 'Hello, world!'

            app.run(debug=True)
        """
        self.debug = debug
        self.shutdown_requested = False

        self.server = socket.socket()
        ai = socket.getaddrinfo(host, port)
        addr = ai[0][-1]

        if self.debug:  # pragma: no cover
            print('Starting {mode} server on {host}:{port}...'.format(
                mode=concurrency_mode, host=host, port=port))
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(addr)
        self.server.listen(5)

        while not self.shutdown_requested:
            try:
                sock, addr = self.server.accept()
            except OSError as exc:  # pragma: no cover
                if exc.args[0] == errno.ECONNABORTED:
                    break
                else:
                    raise
            create_thread(self.dispatch_request, sock, addr)

    def shutdown(self):
        """Request a server shutdown. The server will then exit its request
        listening loop and the :func:`run` function will return. This function
        can be safely called from a route handler, as it only schedules the
        server to terminate as soon as the request completes.

        Example::

            @app.route('/shutdown')
            def shutdown(request):
                request.app.shutdown()
                return 'The server is shutting down...'
        """
        self.shutdown_requested = True

    def find_route(self, req):
        f = None
        for route_methods, route_pattern, route_handler in self.url_map:
            if req.method in route_methods:
                req.url_args = route_pattern.match(req.path)
                if req.url_args is not None:
                    f = route_handler
                    break
        return f

    def dispatch_request(self, sock, addr):
        if not hasattr(sock, 'readline'):  # pragma: no cover
            stream = sock.makefile("rwb")
        else:
            stream = sock

        req = None
        try:
            req = Request.create(self, stream, addr)
        except Exception as exc:  # pragma: no cover
            print_exception(exc)
        if req:
            if req.content_length > req.max_content_length:
                if 413 in self.error_handlers:
                    res = self.error_handlers[413](req)
                else:
                    res = 'Payload too large', 413
            else:
                f = self.find_route(req)
                try:
                    res = None
                    if f:
                        for handler in self.before_request_handlers:
                            res = handler(req)
                            if res:
                                break
                        if res is None:
                            res = f(req, **req.url_args)
                        if isinstance(res, tuple):
                            res = Response(*res)
                        elif not isinstance(res, Response):
                            res = Response(res)
                        for handler in self.after_request_handlers:
                            res = handler(req, res) or res
                    elif 404 in self.error_handlers:
                        res = self.error_handlers[404](req)
                    else:
                        res = 'Not found', 404
                except Exception as exc:
                    print_exception(exc)
                    res = None
                    if exc.__class__ in self.error_handlers:
                        try:
                            res = self.error_handlers[exc.__class__](req, exc)
                        except Exception as exc2:  # pragma: no cover
                            print_exception(exc2)
                    if res is None:
                        if 500 in self.error_handlers:
                            res = self.error_handlers[500](req)
                        else:
                            res = 'Internal server error', 500
        else:
            res = 'Bad request', 400
        if isinstance(res, tuple):
            res = Response(*res)
        elif not isinstance(res, Response):
            res = Response(res)
        res.write(stream)
        stream.close()
        if stream != sock:  # pragma: no cover
            sock.close()
        if self.shutdown_requested:  # pragma: no cover
            self.server.close()
        if self.debug and req:  # pragma: no cover
            print('{method} {path} {status_code}'.format(
                method=req.method, path=req.path,
                status_code=res.status_code))


redirect = Response.redirect
send_file = Response.send_file
