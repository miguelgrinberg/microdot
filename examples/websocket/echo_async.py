from microdot_asyncio import Microdot
from microdot_asyncio_websocket import websocket

app = Microdot()


@app.route('/echo')
@websocket
async def echo(request, ws):
    while True:
        data = await ws.receive()
        await ws.send(data)


app.run()
