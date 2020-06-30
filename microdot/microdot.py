try:
    from sys import print_exception
except ImportError:  # pragma: no cover
    import traceback

    def print_exception(exc):
        traceback.print_exc()

concurrency_mode = 'threaded'

try:  # pragma: no cover
    import threading

    def create_thread(f, *args, **kwargs):
        """Use the threading module."""
        threading.Thread(target=f, args=args, kwargs=kwargs).start()
except ImportError:  # pragma: no cover
    try:
        import _thread

        def create_thread(f, *args, **kwargs):
            """Use MicroPython's _thread module."""
            def run():
                f(*args, **kwargs)

            _thread.start_new_thread(run, ())
    except ImportError:
        def create_thread(f, *args, **kwargs):
            """No threads available, call function synchronously."""
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
    except ImportError:
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


class Request():
    class G:
        pass

    def __init__(self, client_addr, method, url, http_version, headers, body):
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
            if header == 'Content-Length':
                self.content_length = int(value)
            elif header == 'Content-Type':
                self.content_type = value
            elif header == 'Cookie':
                for cookie in value.split(';'):
                    name, value = cookie.strip().split('=', 1)
                    self.cookies[name] = value
        self.body = body
        self._json = None
        self._form = None
        self.g = Request.G()

    @staticmethod
    def create(client_stream, client_addr):
        # request line
        line = client_stream.readline().strip().decode()
        method, url, http_version = line.split()
        http_version = http_version.split('/', 1)[1]

        # headers
        headers = {}
        content_length = 0
        while True:
            line = client_stream.readline().strip().decode()
            if line == '':
                break
            header, value = line.split(':', 1)
            value = value.strip()
            headers[header] = value
            if header == 'Content-Length':
                content_length = int(value)

        # body
        body = client_stream.read(content_length) if content_length else b''

        return Request(client_addr, method, url, http_version, headers, body)

    def _parse_urlencoded(self, urlencoded):
        return {
            urldecode(key): urldecode(value) for key, value in [
                pair.split('=', 1) for pair in
                urlencoded.split('&')]}

    @property
    def json(self):
        if self.content_type != 'application/json':
            return None
        if self._json is None:
            self._json = json.loads(self.body.decode())
        return self._json

    @property
    def form(self):
        if self.content_type != 'application/x-www-form-urlencoded':
            return None
        if self._form is None:
            self._form = self._parse_urlencoded(self.body.decode())
        return self._form


class Response():
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

    def __init__(self, body='', status_code=200, headers=None):
        self.status_code = status_code
        self.headers = headers or {}
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
        stream.write('HTTP/1.0 {status_code} {reason}\r\n'.format(
            status_code=self.status_code,
            reason='OK' if self.status_code == 200 else 'N/A').encode())

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
                if hasattr(self.body, 'close'):
                    self.body.close()
            else:
                stream.write(self.body)

    @classmethod
    def redirect(cls, location, status_code=302):
        return cls(status_code=status_code, headers={'Location': location})

    @classmethod
    def send_file(cls, filename, status_code=200, content_type=None):
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
    def __init__(self):
        self.url_map = []
        self.before_request_handlers = []
        self.after_request_handlers = []
        self.error_handlers = {}
        self.debug = False

    def route(self, url_pattern, methods=None):
        def decorated(f):
            self.url_map.append(
                (methods or ['GET'], URLPattern(url_pattern), f))
            return f
        return decorated

    def before_request(self, f):
        self.before_request_handlers.append(f)
        return f

    def after_request(self, f):
        self.after_request_handlers.append(f)
        return f

    def errorhandler(self, status_code_or_exception_class):
        def decorated(f):
            self.error_handlers[status_code_or_exception_class] = f
            return f
        return decorated

    def run(self, host='0.0.0.0', port=5000, debug=False):
        self.debug = debug

        s = socket.socket()
        ai = socket.getaddrinfo(host, port)
        addr = ai[0][-1]

        if self.debug:  # pragma: no cover
            print('Starting {mode} server on {host}:{port}...'.format(
                mode=concurrency_mode, host=host, port=port))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(5)

        while True:
            sock, addr = s.accept()
            create_thread(self.dispatch_request, sock, addr)

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

        req = Request.create(stream, addr)
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
        if isinstance(res, tuple):
            res = Response(*res)
        elif not isinstance(res, Response):
            res = Response(res)
        res.write(stream)
        stream.close()
        if stream != sock:  # pragma: no cover
            sock.close()
        if self.debug:  # pragma: no cover
            print('{method} {path} {status_code}'.format(
                method=req.method, path=req.path,
                status_code=res.status_code))


redirect = Response.redirect
send_file = Response.send_file
