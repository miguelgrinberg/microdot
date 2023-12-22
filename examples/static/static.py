from microdot import Microdot, send_file
app = Microdot()


@app.route('/')
async def index(request):
    return send_file('static/index.html')


@app.route('/static/<path:path>')
async def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path)


app.run(debug=True)
