try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
from microdot_asyncio import Microdot, Response

app = Microdot()

htmldoc = '''<!DOCTYPE html>
<html>
    <head>
        <title>Microdot Example Page</title>
    </head>
    <body>
        <div>
            <h1>Microdot Example Page</h1>
            <p>Hello from Microdot!</p>
            <p><a href="/shutdown">Click to shutdown the server</a></p>
        </div>
    </body>
</html>
'''


@app.route('/')
async def hello(request):
    return Response(body=htmldoc, headers={'Content-Type': 'text/html'})


@app.route('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


async def main():
    await app.start_server(debug=True)


asyncio.run(main())
