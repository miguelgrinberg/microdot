from microdot import Microdot, Response
from microdot_jinja import render_template

app = Microdot()
Response.default_content_type = 'text/html'


@app.route('/')
def index(req):
    return render_template('page1.html', page='Page 1')


@app.route('/page2')
def page2(req):
    return render_template('page2.html', page='Page 2')


if __name__ == '__main__':
    app.run()
