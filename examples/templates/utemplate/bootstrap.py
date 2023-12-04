from microdot import Microdot, Response
from microdot.utemplate import template

app = Microdot()
Response.default_content_type = 'text/html'


@app.route('/')
async def index(req):
    return template('page1.html').render(page='Page 1')


@app.route('/page2')
async def page2(req):
    return template('page2.html').render(page='Page 2')


if __name__ == '__main__':
    app.run(debug=True)
