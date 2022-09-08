import binascii
import hashlib
import select
import websocket as _websocket
from microdot import Response


class WebSocket:
    CONT = 0
    TEXT = 1
    BINARY = 2
    CLOSE = 8
    PING = 9
    PONG = 10

    def __init__(self, request):
        self.request = request
        self.poll = select.poll()
        self.poll.register(self.request.sock, select.POLLIN)
        self.ws = _websocket.websocket(self.request.sock, True)
        self.request.sock.setblocking(False)

    def handshake(self):
        response = self._handshake_response()
        self.request.sock.write(b'HTTP/1.1 101 Switching Protocols\r\n')
        self.request.sock.write(b'Upgrade: websocket\r\n')
        self.request.sock.write(b'Connection: Upgrade\r\n')
        self.request.sock.write(
            b'Sec-WebSocket-Accept: ' + response + b'\r\n\r\n')

    def receive(self):
        while True:
            self.poll.poll()
            data = self.ws.read()
            if data:
                try:
                    data = data.decode()
                except ValueError:
                    pass
                return data

    def send(self, data):
        self.ws.write(data)

    def close(self):
        self.poll.unregister(self.request.sock)
        self.ws.close()

    def _handshake_response(self):
        for header, value in self.request.headers.items():
            h = header.lower()
            if h == 'connection' and not value.lower().startswith('upgrade'):
                return self.request.app.abort(400)
            elif h == 'upgrade' and not value.lower() == 'websocket':
                return self.request.app.abort(400)
            elif h == 'sec-websocket-key':
                websocket_key = value
        if not websocket_key:
            return self.request.app.abort(400)
        d = hashlib.sha1(websocket_key.encode())
        d.update(b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11')
        return binascii.b2a_base64(d.digest())[:-1]


def websocket_upgrade(request):
    """Upgrade a request handler to a websocket connection.

    This function can be called directly inside a route function to process a
    WebSocket upgrade handshake, for example after the user's credentials are
    verified. The function returns the websocket object::

        @app.route('/echo')
        def echo(request):
            if not authenticate_user(request):
                abort(401)
            ws = websocket_upgrade(request)
            while True:
                message = ws.receive()
                ws.send(message)
    """
    ws = WebSocket(request)
    ws.handshake()

    @request.after_request
    def after_request(request, response):
        return Response.already_handled

    return ws


def with_websocket(f):
    """Decorator to make a route a WebSocket endpoint.

    This decorator is used to define a route that accepts websocket
    connections. The route then receives a websocket object as a second
    argument that it can use to send and receive messages::

        @app.route('/echo')
        @with_websocket
        def echo(request, ws):
            while True:
                message = ws.receive()
                ws.send(message)
    """
    def wrapper(request, *args, **kwargs):
        ws = websocket_upgrade(request)
        try:
            f(request, ws, *args, **kwargs)
        except OSError as exc:
            if exc.errno != 32 and exc.errno != 54:
                raise
        ws.close()
        return ''
    return wrapper
