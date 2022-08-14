import binascii
import hashlib
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
        self.closed = False

    def handshake(self):
        response = self._handshake_response()
        self.request.sock.send(b'HTTP/1.1 101 Switching Protocols\r\n')
        self.request.sock.send(b'Upgrade: websocket\r\n')
        self.request.sock.send(b'Connection: Upgrade\r\n')
        self.request.sock.send(
            b'Sec-WebSocket-Accept: ' + response + b'\r\n\r\n')

    def receive(self):
        while True:
            opcode, payload = self._read_frame()
            send_opcode, data = self._process_websocket_frame(opcode, payload)
            if send_opcode:
                self.send(send_opcode, data)
            elif data:
                return data

    def send(self, data, opcode=None):
        frame = self._encode_websocket_frame(
            opcode or (self.TEXT if isinstance(data, str) else self.BINARY),
            data)
        self.request.sock.send(frame)

    def close(self):
        if not self.closed:
            self.closed = True
            self.send(b'', self.CLOSE)

    def _handshake_response(self):
        for header, value in self.request.headers.items():
            h = header.lower()
            if h == 'connection' and not value.lower().startswith('upgrade'):
                return abort(400)
            elif h == 'upgrade' and not value.lower() == 'websocket':
                return abort(400)
            elif h == 'sec-websocket-key':
                websocket_key = value
        if not websocket_key:
            return abort(400)
        d = hashlib.sha1(websocket_key.encode())
        d.update(b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11')
        return binascii.b2a_base64(d.digest())[:-1]

    def _parse_frame_header(self, header):
        fin = header[0] & 0x80
        opcode = header[0] & 0x0f
        if fin == 0 or opcode == self.CONT:
            self.close()
            raise OSError(32, 'Continuation frames not supported')
        has_mask = header[1] & 0x80
        length = header[1] & 0x7f
        if length == 126:
            length = -2
        elif length == 127:
            length = -8
        return fin, opcode, has_mask, length

    def _process_websocket_frame(self, opcode, payload):
        if opcode == self.TEXT:
            payload = payload.decode()
        elif opcode == self.BINARY:
            pass
        elif opcode == self.CLOSE:
            raise OSError(32, 'Websocket connection closed')
        elif opcode == self.PING:
            return self.PONG, payload
        elif opcode == self.PONG:
            return None, None
        return None, payload

    def _encode_websocket_frame(self, opcode, payload):
        frame = bytearray()
        frame.append(0x80 | opcode)
        if opcode == self.TEXT:
            payload = payload.encode()
        if len(payload) < 126:
            frame.append(len(payload))
        elif len(payload) < (1 << 16):
            frame.append(126)
            frame.extend(payload.length.to_bytes(2, 'big'))
        else:
            frame.append(127)
            frame.extend(payload.length.to_bytes(8, 'big'))
        frame.extend(payload)
        return frame

    def _read_frame(self):
        header = self.request.sock.recv(2)
        fin, opcode, has_mask, length = self._parse_frame_header(header)
        if length == -2:
            length = self.request.sock.recv(2)
            length = int.from_bytes(length, 'big')
        elif length == -8:
            length = self.request.sock.recv(8)
            length = int.from_bytes(length, 'big')
        if has_mask:
            mask = self.request.sock.recv(4)
        payload = self.request.sock.recv(length)
        if has_mask:
            payload = bytes(x ^ mask[i % 4] for i, x in enumerate(payload))
        return opcode, payload


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
                message = ws.recv()
                ws.send(message)
    """
    ws = WebSocket(request)
    ws.handshake()

    @request.after_request
    def after_request(request, response):
        return Response.already_handled

    return ws


def websocket(f):
    """Decorator to make a route a WebSocket endpoint.

    This decorator is used to define a route that accepts websocket
    connections. The route then receives a websocket object as a second
    argument that it can use to send and receive messages::

        @app.route('/echo')
        @websocket
        def echo(request, ws):
            while True:
                message = ws.recv()
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
