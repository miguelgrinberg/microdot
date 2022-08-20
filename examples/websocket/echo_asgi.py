from microdot_asgi import Microdot
from microdot_asgi_websocket import with_websocket

app = Microdot()


@app.route('/echo')
@with_websocket
async def echo(request, ws):
    while True:
        data = await ws.receive()
        await ws.send(data)
