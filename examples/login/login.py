from hashlib import sha1
from microdot import Microdot, redirect
from microdot.session import Session
from microdot.login import Login


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password_hash = self.create_hash(password)

    def create_hash(self, password):
        # note: to keep this example simple, passwords are hashed with the SHA1
        # algorithm. In a real application, you should use a stronger
        # algorithm, such as bcrypt.
        return sha1(password.encode()).hexdigest()

    def check_password(self, password):
        return self.create_hash(password) == self.password_hash

USERS = {
    'user001': User('user001', 'susan', 'hello'),
    'user002': User('user002', 'david', 'bye'),
}

app = Microdot()
Session(app, secret_key='top-secret!')
auth = Login()


@auth.id_to_user
async def get_user(user_id):
    print('get_user', user_id)
    return USERS.get(user_id)


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

    for user in USERS.values():
        if user.username == username:
            if user.check_password(password):
                return await auth.login_user(request, user,
                                             remember=remember_me)
    return redirect('/login')


@app.route('/')
@auth
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
@auth.fresh
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
@auth
async def logout(request):
    await auth.logout_user(request)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
