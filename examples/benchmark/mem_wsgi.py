from microdot_wsgi import Microdot

app = Microdot()


@app.get('/')
def index(req):
    return {'hello': 'world'}
