from microdot import Microdot, redirect
from microdot.session import Session
from microdot.login import Login
from pbkdf2 import generate_password_hash, check_password_hash

# this example provides an implementation of the generate_password_hash and
# check_password_hash functions that can be used in MicroPython. On CPython
# there are many other options for password hashisng so there is no need to use
# this custom solution.


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password_hash = self.create_hash(password)

    def create_hash(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


USERS = {
    'user001': User('user001', 'susan', 'hello'),
    'user002': User('user002', 'david', 'bye'),
}

app = Microdot()
Session(app, secret_key='top-secret!')
login = Login()


@login.user_loader
async def get_user(user_id):
    return USERS.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
async def login_page(request):
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

    for user in USERS.values():
        if user.username == username:
            if user.check_password(password):
                return await login.login_user(request, user,
                                              remember=remember_me)
    return redirect('/login')


@app.route('/')
@login
async def index(request):
    return f'''
        <!doctype html>
        <html>
          <body>
            <h1>Hello, {request.g.current_user.username}!</h1>
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
@login.fresh
async def fresh(request):
    return f'''
        <!doctype html>
        <html>
          <body>
            <h1>Hello, {request.g.current_user.username}!</h1>
            <p>This page requires a fresh login session.</p>
            <p><a href="/">Go back</a> to the main page.</p>
          </body>
        </html>
    ''', {'Content-Type': 'text/html'}


@app.post('/logout')
@login
async def logout(request):
    await login.logout_user(request)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
