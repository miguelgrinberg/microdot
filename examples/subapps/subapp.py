from microdot import Microdot

subapp = Microdot()


@subapp.route('')
async def hello(request):
    # request.url_prefix can be used in links that are relative to this subapp
    return f'''
        <!DOCTYPE html>
        <html>
            <head>
                <title>Microdot Sub-App Example</title>
                <meta charset="UTF-8">
            </head>
            <body>
                <div>
                    <h1>Microdot Sub-App Main Page</h1>
                    <p>Visit the sub-app's <a href="{request.url_prefix}/second">secondary page</a>.</p>
                    <p>Go back to the app's <a href="/">main page</a>.</p>
                </div>
            </body>
        </html>
    ''', 200, {'Content-Type': 'text/html'}  # noqa: E501


@subapp.route('/second')
async def second(request):
    return f'''
        <!DOCTYPE html>
        <html>
            <head>
                <title>Microdot Sub-App Example</title>
                <meta charset="UTF-8">
            </head>
            <body>
                <div>
                    <h1>Microdot Sub-App Secondary Page</h1>
                    <p>Visit the sub-app's <a href="{request.url_prefix}">main page</a>.</p>
                    <p>Go back to the app's <a href="/">main page</a>.</p>
                </div>
            </body>
        </html>
    ''', 200, {'Content-Type': 'text/html'}  # noqa: E501
