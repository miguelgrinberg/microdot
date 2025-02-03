from microdot import Microdot
from microdot.auth import BasicAuth
from pbkdf2 import generate_password_hash, check_password_hash


# this example provides an implementation of the generate_password_hash and
# check_password_hash functions that can be used in MicroPython. On CPython
# there are many other options for password hashisng so there is no need to use
# this custom solution.
USERS = {
    'susan': generate_password_hash('hello'),
    'david': generate_password_hash('bye'),
}
app = Microdot()
auth = BasicAuth()


@auth.authenticate
async def check_credentials(request, username, password):
    if username in USERS and check_password_hash(USERS[username], password):
        return username


@app.route('/')
@auth
async def index(request):
    return f'Hello, {request.g.current_user}!'


if __name__ == '__main__':
    app.run(debug=True)
