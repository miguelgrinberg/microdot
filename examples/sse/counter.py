import asyncio
from microdot import Microdot, send_file
from microdot.sse import with_sse

app = Microdot()


@app.route("/")
async def main(request):
    return send_file('index.html')


@app.route('/events')
@with_sse
async def events(request, sse):
    print('Client connected')
    try:
        i = 0
        while True:
            await asyncio.sleep(1)
            i += 1
            await sse.send({'counter': i})
    except asyncio.CancelledError:
        pass
    print('Client disconnected')


app.run()
