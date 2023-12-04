from microdot import Microdot
from microdot.cors import CORS

app = Microdot()
CORS(app, allowed_origins=['https://example.org'], allow_credentials=True)


@app.route('/')
def index(request):
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
