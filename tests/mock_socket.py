try:
    import uio as io
except ImportError:
    import io

SOL_SOCKET = 'SOL_SOCKET'
SO_REUSEADDR = 'SO_REUSEADDR'

_requests = []


def getaddrinfo(host, port):
    return (('family', 'addr'), 'socktype', 'proto', 'canonname', 'sockaddr')


class socket:
    def __init__(self):
        self.request_index = 0

    def setsockopt(self, level, optname, value):
        pass

    def bind(self, addr):
        pass

    def listen(self, backlog):
        pass

    def accept(self):
        self.request_index += 1
        return _requests[self.request_index - 1], 'addr'

    def close(self):
        pass


class FakeStream(io.BytesIO):
    def __init__(self, input_data):
        super().__init__(input_data)
        self.response = b''

    def write(self, data):
        self.response += data


class FakeStreamAsync:
    def __init__(self, stream=None):
        if stream is None:
            stream = FakeStream(b'')
        self.stream = stream

    @property
    def response(self):
        return self.stream.response

    async def readline(self):
        return self.stream.readline()

    async def read(self, n=-1):
        return self.stream.read(n)

    async def readexactly(self, n):
        return self.stream.read(n)

    async def awrite(self, data):
        self.stream.write(data)

    async def aclose(self):
        pass

    def get_extra_info(self, name, default=None):
        return name


def get_request_fd(method, path, headers=None, body=None):
    if headers is None:
        headers = {}
    if body is None:
        body = ''
    elif 'Content-Length' not in headers:
        headers['Content-Length'] = str(len(body))
    request_bytes = '{method} {path} HTTP/1.0\n'.format(
        method=method, path=path)
    if 'Host' not in headers:
        headers['Host'] = 'example.com:1234'
    for header, value in headers.items():
        request_bytes += '{header}: {value}\n'.format(
            header=header, value=value)
    request_bytes += '\n' + body
    return FakeStream(request_bytes.encode())


def get_async_request_fd(method, path, headers=None, body=None):
    fd = get_request_fd(method, path, headers=headers, body=body)
    return FakeStreamAsync(fd)


def clear_requests():
    _requests.clear()


def add_request(method, path, headers=None, body=None):
    fd = get_request_fd(method, path, headers=headers, body=body)
    _requests.append(fd)
    return fd
