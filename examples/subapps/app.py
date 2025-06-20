from microdot import Microdot
from subapp import subapp

app = Microdot()
app.mount(subapp, url_prefix='/subapp')


@app.route('/')
async def hello(request):
    return '''
        <!DOCTYPE html>
        <html>
            <head>
                <title>Microdot Sub-App Example</title>
                <meta charset="UTF-8">
            </head>
            <body>
                <div>
                    <h1>Microdot Main Page</h1>
                    <p>Visit the <a href="/subapp">sub-app</a>.</p>
                </div>
            </body>
        </html>
    ''', 200, {'Content-Type': 'text/html'}


app.run(debug=True)
