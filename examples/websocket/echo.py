from microdot import Microdot
from microdot_websocket import with_websocket

app = Microdot()


@app.route('/echo')
@with_websocket
def echo(request, ws):
    while True:
        data = ws.receive()
        ws.send(data)


app.run()
