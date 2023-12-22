from microdot import Microdot, Response
from microdot.utemplate import template

app = Microdot()
Response.default_content_type = 'text/html'


@app.route('/', methods=['GET', 'POST'])
async def index(req):
    name = None
    if req.method == 'POST':
        name = req.form.get('name')
    return await template('index.html').render_async(name=name)


if __name__ == '__main__':
    app.run()
