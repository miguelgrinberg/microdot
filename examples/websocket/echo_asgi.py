from microdot.asgi import Microdot, send_file, with_websocket

app = Microdot()


@app.route('/')
async def index(request):
    return send_file('index.html')


@app.route('/echo')
@with_websocket
async def echo(request, ws):
    while True:
        data = await ws.receive()
        await ws.send(data)


if __name__ == '__main__':
    app.run()
