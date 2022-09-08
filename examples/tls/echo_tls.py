import sys
from microdot import Microdot, send_file
from microdot_websocket import with_websocket
from microdot_ssl import create_ssl_context

app = Microdot()


@app.route('/')
def index(request):
    return send_file('index.html')


@app.route('/echo')
@with_websocket
def echo(request, ws):
    while True:
        data = ws.receive()
        ws.send(data)


ext = 'der' if sys.implementation.name == 'micropython' else 'pem'
sslctx = create_ssl_context('cert.' + ext, 'key.' + ext)
app.run(port=4443, debug=True, ssl=sslctx)
