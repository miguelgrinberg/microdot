from microdot import Microdot
from microdot_auth import BasicAuth

app = Microdot()
basic_auth = BasicAuth()

USERS = {
    'susan': 'hello',
    'david': 'bye',
}


@basic_auth.callback
def verify_password(request, username, password):
    if username in USERS and USERS[username] == password:
        request.g.user = username
        return True


@app.route('/')
@basic_auth
def index(request):
    return f'Hello, {request.g.user}!'


if __name__ == '__main__':
    app.run(debug=True)
