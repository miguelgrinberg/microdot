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
    import socket


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
    def __init__(self, client_sock, client_addr):
        self.client_sock = client_sock
        self.client_addr = client_addr

        if not hasattr(client_sock, 'readline'):
            self.client_stream = client_sock.makefile("rwb")
        else:
            self.client_stream = client_sock

        # request line
        line = self.client_stream.readline().strip().decode('utf-8')
        self.method, self.path, self.http_version = line.split()
        if '?' in self.path:
            self.path, self.query_string = self.path.split('?', 1)
        else:
            self.query_string = None

        # headers
        self.headers = {}
        self.cookies = {}
        self.content_length = 0
        while True:
            line = self.client_stream.readline().strip().decode('utf-8')
            if line == '':
                break
            header, value = line.split(':', 1)
            value = value.strip()
            self.headers[header] = value
            if header == 'Content-Length':
                self.content_length = int(value)
            elif header == 'Content-Type':
                self.content_type = value
            elif header == 'Cookie':
                for cookie in self.headers['Cookie'].split(';'):
                    name, value = cookie.split('=', 1)
                    self.cookies[name] = value

        # body
        self.body = self.client_stream.read(self.content_length)
        self._json = None
        self._form = None

    @property
    def json(self):
        if self.content_type != 'application/json':
            return None
        if self._json is None:
            self._json = json.loads(self.body)
        return self._json

    @property
    def form(self):
        if self.content_type != 'application/x-www-form-urlencoded':
            return None
        if self._form is None:
            self._form = {urldecode(key): urldecode(value) for key, value in
                          [pair.split('=', 1) for pair in self.body.decode().split('&')]}
        return self._form

    def close(self):
        self.client_stream.close()
        if self.client_stream != self.client_sock:
            self.client_sock.close()


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

    def __init__(self, body='', status_code=200, headers=None):
        self.status_code = status_code
        self.headers = headers or {}
        self.cookies = []
        if isinstance(body, (dict, list)):
            self.body = json.dumps(body).encode()
            self.headers['Content-Type'] = 'application/json'
        elif isinstance(body, str):
            self.body = body.encode()
        elif isinstance(body, bytes):
            self.body = body
        else:
            self.body = str(body).encode()

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
            http_cookie += '; httpOnly'
        if 'Set-Cookie' in self.headers:
            self.headers['Set-Cookie'].append(http_cookie)
        else:
            self.headers['Set-Cookie'] = [http_cookie]

    def write(self, client_stream):
        # status code
        client_stream.write('HTTP/1.0 {status_code} {reason}\r\n'.format(
            status_code=self.status_code,
            reason='OK' if self.status_code == 200 else 'N/A').encode())

        # headers
        content_length_found = False
        content_type_found = False
        for header, value in self.headers.items():
            values = value if isinstance(value, list) else [value]
            for value in values:
                client_stream.write('{header}: {value}\r\n'.format(
                    header=header, value=value).encode())
            if header == 'Content-Length':
                content_length_found = True
            elif header == 'Content-Type':
                content_type_found = True
        if not content_length_found:
            client_stream.write('Content-Length: {length}\r\n'.format(
                length=len(self.body)).encode())
        if not content_type_found:
            client_stream.write(b'Content-Type: text/plain\r\n')
        client_stream.write(b'\r\n')

        # body
        if self.body:
            client_stream.write(self.body)

    @staticmethod
    def redirect(location, status_code=302):
        return Response(status_code=status_code,
                        headers={'Location': location})

    @staticmethod
    def send_file(filename, status_code=200, content_type=None):
        if content_type is None:
            ext = filename.split('.')[-1]
            if ext in Response.types_map:
                content_type = Response.types_map[ext]
            else:
                content_type = 'application/octet-stream'
        with open(filename) as f:
            return Response(body=f.read(), status_code=status_code,
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
                    type_, name = segment.split(':', 1)
                else:
                    type_ = 'string'
                    name = segment
                if type_ == 'string':
                    pattern = '[^/]*'
                elif type_ == 'int':
                    pattern = '\\d+'
                elif type_ == 'path':
                    pattern = '.*'
                elif type_.startswith('regex'):
                    pattern = eval(type_[5:])
                else:
                    raise ValueError('invalid URL segment type')
                use_regex = True
                self.pattern += '/({pattern})'.format(pattern=pattern)
                self.args.append({'type': type_, 'name': name})
            else:
                self.pattern += '/{segment}'.format(segment=segment)
        if use_regex:
            self.pattern = re.compile(self.pattern)

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
    def __init__(self) :
        self.url_map = []

    def route(self, url_pattern, methods=None):
        def decorated(f):
            self.url_map.append(
                (methods or ['GET'], URLPattern(url_pattern), f))
            return f
        return decorated

    def run(self, host='0.0.0.0', port=5000):
        s = socket.socket()
        ai = socket.getaddrinfo(host, port)
        addr = ai[0][-1]

        print('Listening on {host}:{port}...'.format(host=host, port=port))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(5)

        while True:
            req = Request(*s.accept())
            f = None
            args = None
            for route_methods, route_pattern, route_handler in self.url_map:
                if req.method in route_methods:
                    args = route_pattern.match(req.path)
                    if args is not None:
                        f = route_handler
                        break
            if f:
                resp = f(req, **args)
                if isinstance(resp, tuple):
                    resp = Response(*resp)
                elif not isinstance(resp, Response):
                    resp = Response(resp)
                resp.write(req.client_stream)
                req.close()


redirect = Response.redirect
send_file = Response.send_file
