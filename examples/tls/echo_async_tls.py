import ssl
from microdot_asyncio import Microdot, send_file
from microdot_asyncio_websocket import with_websocket

app = Microdot()


@app.route('/')
def index(request):
    return send_file('index.html')


@app.route('/echo')
@with_websocket
async def echo(request, ws):
    while True:
        data = await ws.receive()
        await ws.send(data)


sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
sslctx.load_cert_chain('cert.pem', 'key.pem')
app.run(port=4443, debug=True, ssl=sslctx)
