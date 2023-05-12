import sys
from microdot import Microdot
from microdot_ssl import create_ssl_context

app = Microdot()

htmldoc = '''<!DOCTYPE html>
<html>
    <head>
        <title>Microdot Example Page</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <div>
            <h1>Microdot Example Page</h1>
            <p>Hello from Microdot!</p>
            <p><a href="/shutdown">Click to shutdown the server</a></p>
        </div>
    </body>
</html>
'''


@app.route('/')
def hello(request):
    return htmldoc, 200, {'Content-Type': 'text/html'}


@app.route('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


ext = 'der' if sys.implementation.name == 'micropython' else 'pem'
sslctx = create_ssl_context('cert.' + ext, 'key.' + ext)
app.run(port=4443, debug=True, ssl=sslctx)
