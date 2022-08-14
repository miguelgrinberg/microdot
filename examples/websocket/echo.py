from microdot import Microdot
from microdot_websocket import websocket

app = Microdot()


@app.route('/echo')
@websocket
def echo(request, ws):
    while True:
        data = ws.receive()
        ws.send(data)


app.run()
