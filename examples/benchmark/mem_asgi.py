from microdot.asgi import Microdot

app = Microdot()


@app.get('/')
async def index(req):
    return {'hello': 'world'}
