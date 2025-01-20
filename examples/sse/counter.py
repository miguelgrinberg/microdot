import asyncio
from microdot import Microdot
from microdot.sse import with_sse

app = Microdot()


@app.route("/")
async def main(request):
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Microdot SSE Example</title>
            <meta charset="UTF-8">
        </head>
        <body>
            <h1>Microdot SSE Example</h1>
            <script>
            // Create a new EventSource instance with the endpoint URL
            const eventSource = new EventSource('/events');

            // Listen for incoming messages
            eventSource.onmessage = (event) => {
                console.log('Received message:', event.data);
            };

            // Handle connection errors
            eventSource.onerror = (error) => {
                console.error('EventSource failed:', error);
            };

            // Optionally handle connection opening
            eventSource.onopen = () => {
                console.log('Connection to server opened.');
            };
            </script>
        </body>
    </html>
    """
    return html, 200, {'Content-Type': 'text/html'}


@app.route('/events')
@with_sse
async def events(request, sse):
    i = 0
    while True:
        await asyncio.sleep(1)
        i += 1
        await sse.send({'counter': i})

app.run()