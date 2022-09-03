from microdot_asyncio import Response
from microdot_websocket import WebSocket as BaseWebSocket


class WebSocket(BaseWebSocket):
    async def handshake(self):
        response = self._handshake_response()
        await self.request.sock[1].awrite(
            b'HTTP/1.1 101 Switching Protocols\r\n')
        await self.request.sock[1].awrite(b'Upgrade: websocket\r\n')
        await self.request.sock[1].awrite(b'Connection: Upgrade\r\n')
        await self.request.sock[1].awrite(
            b'Sec-WebSocket-Accept: ' + response + b'\r\n\r\n')

    async def receive(self):
        while True:
            opcode, payload = await self._read_frame()
            send_opcode, data = self._process_websocket_frame(opcode, payload)
            if send_opcode:  # pragma: no cover
                await self.send(send_opcode, data)
            elif data:  # pragma: no branch
                return data

    async def send(self, data, opcode=None):
        frame = self._encode_websocket_frame(
            opcode or (self.TEXT if isinstance(data, str) else self.BINARY),
            data)
        await self.request.sock[1].awrite(frame)

    async def close(self):
        if not self.closed:  # pragma: no cover
            self.closed = True
            await self.send(b'', self.CLOSE)

    async def _read_frame(self):
        header = await self.request.sock[0].read(2)
        if len(header) != 2:  # pragma: no cover
            raise OSError(32, 'Websocket connection closed')
        fin, opcode, has_mask, length = self._parse_frame_header(header)
        if length == -2:
            length = await self.request.sock[0].read(2)
            length = int.from_bytes(length, 'big')
        elif length == -8:
            length = await self.request.sock[0].read(8)
            length = int.from_bytes(length, 'big')
        if has_mask:  # pragma: no cover
            mask = await self.request.sock[0].read(4)
        payload = await self.request.sock[0].read(length)
        if has_mask:  # pragma: no cover
            payload = bytes(x ^ mask[i % 4] for i, x in enumerate(payload))
        return opcode, payload


async def websocket_upgrade(request):
    """Upgrade a request handler to a websocket connection.

    This function can be called directly inside a route function to process a
    WebSocket upgrade handshake, for example after the user's credentials are
    verified. The function returns the websocket object::

        @app.route('/echo')
        async def echo(request):
            if not authenticate_user(request):
                abort(401)
            ws = await websocket_upgrade(request)
            while True:
                message = await ws.receive()
                await ws.send(message)
    """
    ws = WebSocket(request)
    await ws.handshake()

    @request.after_request
    async def after_request(request, response):
        return Response.already_handled

    return ws


def with_websocket(f):
    """Decorator to make a route a WebSocket endpoint.

    This decorator is used to define a route that accepts websocket
    connections. The route then receives a websocket object as a second
    argument that it can use to send and receive messages::

        @app.route('/echo')
        @with_websocket
        async def echo(request, ws):
            while True:
                message = await ws.receive()
                await ws.send(message)
    """
    async def wrapper(request, *args, **kwargs):
        ws = await websocket_upgrade(request)
        try:
            await f(request, ws, *args, **kwargs)
            await ws.close()  # pragma: no cover
        except OSError as exc:
            if exc.errno not in [32, 54, 104]:  # pragma: no cover
                raise
        return ''
    return wrapper
