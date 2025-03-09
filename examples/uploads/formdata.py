from microdot import Microdot, send_file, Request
from microdot.multipart import with_form_data

app = Microdot()
Request.max_content_length = 1024 * 1024  # 1MB (change as needed)


@app.get('/')
async def index(request):
    return send_file('formdata.html')


@app.post('/')
@with_form_data
async def upload(request):
    print(request.form)
    for file in request.files.values():
        print(file.filename, await file.read())
    return 'We have received your data!'


if __name__ == '__main__':
    app.run(debug=True)
