from microdot import Microdot, send_file

app = Microdot()


@app.get('/')
def index(request):
    return send_file('index.html')


@app.post('/upload')
def upload(request):
    # obtain the filename and size from request headers
    filename = request.headers['Content-Disposition'].split(
        'filename=')[1].strip('"')
    size = int(request.headers['Content-Length'])

    # sanitize the filename
    filename = filename.replace('/', '_')

    # write the file to the files directory in 1K chunks
    with open('files/' + filename, 'wb') as f:
        while size > 0:
            chunk = request.stream.read(min(size, 1024))
            f.write(chunk)
            size -= len(chunk)

    print('Successfully saved file: ' + filename)
    return ''


if __name__ == '__main__':
    app.run()
