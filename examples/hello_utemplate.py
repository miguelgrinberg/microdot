from microdot import Microdot, Response
from microdot_utemplate import render_template

app = Microdot()
Response.default_content_type = 'text/html'


@app.route('/', methods=['GET', 'POST'])
def index(req):
    name = None
    if req.method == 'POST':
        name = req.form.get('name')
    return render_template('index.html', name=name)


if __name__ == '__main__':
    app.run()
