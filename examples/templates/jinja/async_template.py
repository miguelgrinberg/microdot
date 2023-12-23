from microdot import Microdot, Response
from microdot.jinja import Template

Template.initialize('templates', enable_async=True)
app = Microdot()
Response.default_content_type = 'text/html'


@app.route('/', methods=['GET', 'POST'])
async def index(req):
    name = None
    if req.method == 'POST':
        name = req.form.get('name')
    return await Template('index.html').render_async(name=name)


if __name__ == '__main__':
    app.run()
