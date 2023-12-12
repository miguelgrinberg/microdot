import asyncio
from microdot import Microdot
from microdot.sse import with_sse

app = Microdot()


@app.route('/events')
@with_sse
async def events(request, sse):
    for i in range(10):
        await asyncio.sleep(1)
        await sse.send({'counter': i})


app.run(debug=True)
