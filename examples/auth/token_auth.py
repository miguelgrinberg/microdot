from microdot import Microdot
from microdot_auth import TokenAuth

app = Microdot()
token_auth = TokenAuth()

TOKENS = {
    'hello': 'susan',
    'bye': 'david',
}


@token_auth.callback
def verify_token(request, token):
    if token in TOKENS:
        request.g.user = TOKENS[token]
        return True


@app.route('/')
@token_auth
def index(request):
    return f'Hello, {request.g.user}!'


if __name__ == '__main__':
    app.run(debug=True)
