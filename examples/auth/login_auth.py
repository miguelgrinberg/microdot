from microdot import Microdot, redirect
from microdot_session import set_session_secret_key
from microdot_login import LoginAuth

app = Microdot()
set_session_secret_key('top-secret')
login_auth = LoginAuth()

USERS = {
    'susan': 'hello',
    'david': 'bye',
}


@login_auth.callback
def check_user(request, user_id):
    request.g.user = user_id
    return True


@app.route('/')
@login_auth
def index(request):
    return f'''
        <h1>Login Auth Example</h1>
        <p>Hello, {request.g.user}!</p>
        <form method="POST" action="/logout">
            <button type="submit">Logout</button>
        </form>
    ''', {'Content-Type': 'text/html'}


@app.route('/login', methods=['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        return '''
            <h1>Login Auth Example</h1>
            <form method="POST">
                <input name="username" placeholder="username">
                <input name="password" type="password" placeholder="password">
                <button type="submit">Login</button>
            </form>
        ''', {'Content-Type': 'text/html'}
    username = request.form['username']
    password = request.form['password']
    if USERS.get(username) == password:
        login_auth.login_user(request, username)
        return login_auth.redirect_to_next(request)
    else:
        return redirect('/login')


@app.post('/logout')
def logout(request):
    login_auth.logout_user(request)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
