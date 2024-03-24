from hashlib import sha1
from microdot import Microdot, redirect
from microdot.session import Session
from microdot.auth import LoginAuth


def create_hash(password):
    return sha1(password).hexdigest()


USERS = {
    'susan': create_hash(b'hello'),
    'david': create_hash(b'bye'),
}

app = Microdot()
Session(app, secret_key='top-secret!')
auth = LoginAuth()


@auth.id_to_user
async def get_user(user_id):
    return user_id


@auth.user_to_id
async def get_user_id(user):
    return user


@app.route('/')
@auth
async def index(request):
    return f'''
        <h1>Login Auth Example</h1>
        <p>Hello, {request.g.current_user}!</p>
        <form method="POST" action="/logout">
            <button type="submit">Logout</button>
        </form>
    ''', {'Content-Type': 'text/html'}


@app.route('/login', methods=['GET', 'POST'])
async def login(request):
    if request.method == 'GET':
        return '''
            <h1>Login Auth Example</h1>
            <form method="POST">
                <input name="username" placeholder="username" autofocus>
                <input name="password" type="password" placeholder="password">
                <br><input name="remember_me" type="checkbox"> Remember me
                <br><button type="submit">Login</button>
            </form>
        ''', {'Content-Type': 'text/html'}
    username = request.form['username']
    password = request.form['password']
    remember_me = bool(request.form.get('remember_me'))
    if USERS.get(username) == create_hash(password.encode()):
        return await auth.login_user(request, username, remember=remember_me)
    else:
        return redirect('/login')


@app.get('/fresh')
@auth.fresh
async def fresh(request):
    return '''
        <h1>Fresh Login only</h1>
    ''', {'Content-Type': 'text/html'}


@app.post('/logout')
@auth
async def logout(request):
    await auth.logout_user(request)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
