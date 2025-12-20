from microdot import Microdot, redirect
from microdot.cors import CORS
from microdot.csrf import CSRF

app = Microdot()
cors = CORS(app, allowed_origins=['http://localhost:5000'])
csrf = CSRF(app, cors)

balance = 1000


@app.route('/', methods=['GET', 'POST'])
def index(request):
    global balance
    if request.method == 'POST':
        try:
            balance -= float(request.form['amount'])
        except ValueError:
            pass
        return redirect('/')

    page = f'''<!doctype html>
<html>
  <head>
    <title>CSRF Example</title>
  </head>
  <body>
    <h1>CSRF Example</h1>
    <p>You have ${balance:.02f}</p>
    <form method="POST" action="">
      Pay $<input type="text" name="amount" size="10" />
      <input type="submit" value="Issue Payment" />
    </form>
  </body>
</html>'''
    return page, {'Content-Type': 'text/html'}


if __name__ == '__main__':
    app.run(debug=True)
