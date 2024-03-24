from microdot import Microdot
from microdot.auth import TokenAuth

app = Microdot()
auth = TokenAuth()

TOKENS = {
    'susan-token': 'susan',
    'david-token': 'david',
}


@auth.authenticate
async def check_token(request, token):
    if token in TOKENS:
        return TOKENS[token]


@app.route('/')
@auth
async def index(request):
    return f'Hello, {request.g.current_user}!'


if __name__ == '__main__':
    app.run(debug=True)
