from microdot import Microdot, send_file

app = Microdot()


@app.route('/')
def index(request):
    return send_file('gzstatic/index.html', compressed=True,
                     file_extension='.gz')


@app.route('/static/<path:path>')
def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('gzstatic/' + path, compressed=True, file_extension='.gz')


app.run(debug=True)
