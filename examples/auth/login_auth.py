from hashlib import sha1
from microdot import Microdot, redirect
from microdot.session import Session
from microdot.auth import Login


def create_hash(password):
    return sha1(password).hexdigest()


USERS = {
    'susan': create_hash(b'hello'),
    'david': create_hash(b'bye'),
}

app = Microdot()
Session(app, secret_key='top-secret!')
auth = Login()


@auth.id_to_user
async def get_user(user_id):
    return user_id


@auth.user_to_id
async def get_user_id(user):
    return user


@app.route('/login', methods=['GET', 'POST'])
async def login(request):
    if request.method == 'GET':
        return '''
            <!doctype html>
            <html>
              <body>
                <h1>Please Login</h1>
                <form method="POST">
                  <p>
                    Username<br>
                    <input name="username" autofocus>
                  </p>
                  <p>
                    Password:<br>
                    <input name="password" type="password">
                    <br>
                  </p>
                  <p>
                    <input name="remember_me" type="checkbox"> Remember me
                    <br>
                  </p>
                  <p>
                    <button type="submit">Login</button>
                  </p>
                </form>
              </body>
            </html>
        ''', {'Content-Type': 'text/html'}
    username = request.form['username']
    password = request.form['password']
    remember_me = bool(request.form.get('remember_me'))
    if USERS.get(username) == create_hash(password.encode()):
        return await auth.login_user(request, username, remember=remember_me)
    else:
        return redirect('/login')


@app.route('/')
@auth
async def index(request):
    return f'''
        <!doctype html>
        <html>
          <body>
            <h1>Hello, {request.g.current_user}!</h1>
            <p>
              <a href="/fresh">Click here</a> to access the fresh login page.
            </p>
            <form method="POST" action="/logout">
              <button type="submit">Logout</button>
            </form>
          </body>
        </html>
    ''', {'Content-Type': 'text/html'}


@app.get('/fresh')
@auth.fresh
async def fresh(request):
    return f'''
        <!doctype html>
        <html>
          <body>
            <h1>Hello, {request.g.current_user}!</h1>
            <p>This page requires a fresh login session.</p>
            <p><a href="/">Go back</a> to the main page.</p>
          </body>
        </html>
    ''', {'Content-Type': 'text/html'}


@app.post('/logout')
@auth
async def logout(request):
    await auth.logout_user(request)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
