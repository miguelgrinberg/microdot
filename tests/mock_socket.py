try:
    import uio as io
except ImportError:
    import io

SOL_SOCKET = 'SOL_SOCKET'
SO_REUSEADDR = 'SO_REUSEADDR'

_calls = []
_requests = []


def getaddrinfo(host, port):
    _calls.append(('getaddrinfo', host, port))
    return (('family', 'addr'), 'socktype', 'proto', 'canonname', 'sockaddr')


class socket:
    def __init__(self):
        self.request_index = 0

    def setsockopt(self, level, optname, value):
        _calls.append(('setsockopt', level, optname, value))

    def bind(self, addr):
        _calls.append(('bind', addr))

    def listen(self, backlog):
        _calls.append(('listen', backlog))

    def accept(self):
        _calls.append(('accept',))
        self.request_index += 1
        return _requests[self.request_index - 1], 'addr'


class FakeStream(io.BytesIO):
    def __init__(self, input_data):
        super().__init__(input_data)
        self.response = b''

    def write(self, data):
        self.response += data


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


def clear_requests():
    _requests.clear()


def add_request(method, path, headers=None, body=None):
    fd = get_request_fd(method, path, headers=headers, body=body)
    _requests.append(fd)
    return fd
