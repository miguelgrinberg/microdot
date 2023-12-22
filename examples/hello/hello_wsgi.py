from microdot.wsgi import Microdot

app = Microdot()

html = '''<!DOCTYPE html>
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
    return html, 200, {'Content-Type': 'text/html'}


@app.route('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


if __name__ == '__main__':
    print('''Use a WSGI web server to run this applicaton.
Example:
    gunicorn hello_wsgi:app
''')
