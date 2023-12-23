from microdot import Microdot, Response
from microdot.jinja import Template

app = Microdot()
Response.default_content_type = 'text/html'


@app.route('/')
async def index(req):
    return Template('page1.html').render(page='Page 1')


@app.route('/page2')
async def page2(req):
    return Template('page2.html').render(page='Page 2')


if __name__ == '__main__':
    app.run()
