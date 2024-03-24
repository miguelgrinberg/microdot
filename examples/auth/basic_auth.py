from hashlib import sha1
from microdot import Microdot
from microdot.auth import BasicAuth


def create_hash(password):
    return sha1(password).hexdigest()


USERS = {
    'susan': create_hash(b'hello'),
    'david': create_hash(b'bye'),
}
app = Microdot()
auth = BasicAuth()


@auth.authenticate
async def check_credentials(request, username, password):
    if username in USERS and USERS[username] == create_hash(password.encode()):
        return username


@app.route('/')
@auth
async def index(request):
    return f'Hello, {request.g.current_user}!'


if __name__ == '__main__':
    app.run(debug=True)
