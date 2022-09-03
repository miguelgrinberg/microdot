from microdot import Microdot, send_file
from microdot_websocket import with_websocket

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


app.run()
