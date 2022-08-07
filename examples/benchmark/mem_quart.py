from quart import Quart

app = Quart(__name__)


@app.get('/')
def index():
    return {'hello': 'world'}
