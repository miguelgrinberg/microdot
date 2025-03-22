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
    print('Form fields:')
    for field, value in request.form.items():
        print(f'- {field}: {value}')
    print('\nFile uploads:')
    for field, value in request.files.items():
        print(f'- {field}: {value.filename}, {await value.read()}')
    return 'We have received your data!'


if __name__ == '__main__':
    app.run(debug=True)
