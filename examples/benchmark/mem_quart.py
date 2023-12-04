from quart import Quart

app = Quart(__name__)


@app.get('/')
async def index():
    return {'hello': 'world'}
