from microdot import Microdot

app = Microdot()


@app.get('/')
def index(req):
    return {'hello': 'world'}


app.run()
