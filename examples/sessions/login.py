# This is a simple example that demonstrates how to use the user session, but
# is not intended as a complete login solution. See the login subdirectory for
# a more complete example.
from microdot import Microdot, Response, redirect
from microdot.session import Session, with_session

BASE_TEMPLATE = '''<!doctype html>
<html>
  <head>
    <title>Microdot login example</title>
    <meta charset="UTF-8">
  </head>
  <body>
    <h1>Microdot login example</h1>
    {content}
  </body>
</html>'''

LOGGED_OUT = '''<p>You are not logged in.</p>
<form method="POST">
  <p>
    Username:
    <input name="username" autofocus />
  </p>
  <input type="submit" value="Submit" />
</form>'''

LOGGED_IN = '''<p>Hello <b>{username}</b>!</p>
<form method="POST" action="/logout">
  <input type="submit" value="Logout" />
</form>'''

app = Microdot()
Session(app, secret_key='top-secret')
Response.default_content_type = 'text/html'


@app.get('/')
@app.post('/')
@with_session
async def index(req, session):
    username = session.get('username')
    if req.method == 'POST':
        username = req.form.get('username')
        session['username'] = username
        session.save()
        return redirect('/')
    if username is None:
        return BASE_TEMPLATE.format(content=LOGGED_OUT)
    else:
        return BASE_TEMPLATE.format(content=LOGGED_IN.format(
            username=username))


@app.post('/logout')
@with_session
async def logout(req, session):
    session.delete()
    return redirect('/')


if __name__ == '__main__':
    app.run()
