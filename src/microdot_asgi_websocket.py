from microdot_asyncio import Response, abort
from microdot_websocket import WebSocket as BaseWebSocket


class WebSocket(BaseWebSocket):
    async def handshake(self):
        connect = await self.request.sock[0]()
        if connect['type'] != 'websocket.connect':
            abort(400)
        await self.request.sock[1]({'type': 'websocket.accept'})

    async def receive(self):
        message = await self.request.sock[0]()
        if message['type'] == 'websocket.disconnect':
            raise OSError(32, 'Websocket connection closed')
        elif message['type'] != 'websocket.receive':
            raise OSError(32, 'Websocket message type not supported')
        return message.get('bytes', message.get('text'))

    async def send(self, data):
        if isinstance(data, str):
            await self.request.sock[1](
                {'type': 'websocket.send', 'text': data})
        else:
            await self.request.sock[1](
                {'type': 'websocket.send', 'bytes': data})

    async def close(self):
        if not self.closed:
            self.closed = True
            try:
                await self.request.sock[1]({'type': 'websocket.close'})
            except:  # noqa E722
                pass


async def websocket_upgrade(request):
    """Upgrade a request handler to a websocket connection.

    This function can be called directly inside a route function to process a
    WebSocket upgrade handshake, for example after the user's credentials are
    verified. The function returns the websocket object::

        @app.route('/echo')
        async def echo(request):
            if not (await authenticate_user(request)):
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
        except OSError as exc:
            if exc.errno != 32 and exc.errno != 54:
                raise
        await ws.close()
        return ''
    return wrapper
