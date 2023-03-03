from microdot.asyncio import Microdot

app = Microdot()


@app.get('/')
async def index(req):
    return {'hello': 'world'}


app.run()
