import sys
import asyncio
from microdot import Microdot

app = Microdot()

frames = []
for file in ['1.jpg', '2.jpg', '3.jpg']:
    with open(file, 'rb') as f:
        frames.append(f.read())


@app.route('/')
async def index(request):
    return '''<!doctype html>
<html>
  <head>
    <title>Microdot Video Streaming</title>
    <meta charset="UTF-8">
  </head>
  <body>
    <h1>Microdot Video Streaming</h1>
    <img src="/video_feed">
  </body>
</html>''', 200, {'Content-Type': 'text/html'}


@app.route('/video_feed')
async def video_feed(request):
    print('Starting video stream.')

    if sys.implementation.name != 'micropython':
        # CPython supports async generator function
        async def stream():
            try:
                yield b'--frame\r\n'
                while True:
                    for frame in frames:
                        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + \
                            b'\r\n--frame\r\n'
                        await asyncio.sleep(1)
            except GeneratorExit:
                print('Stopping video stream.')
    else:
        # MicroPython can only use class-based async generators
        class stream():
            def __init__(self):
                self.i = 0

            def __aiter__(self):
                return self

            async def __anext__(self):
                await asyncio.sleep(1)
                self.i = (self.i + 1) % len(frames)
                return b'Content-Type: image/jpeg\r\n\r\n' + \
                    frames[self.i] + b'\r\n--frame\r\n'

            async def aclose(self):
                print('Stopping video stream.')

    return stream(), 200, {'Content-Type':
                           'multipart/x-mixed-replace; boundary=frame'}


if __name__ == '__main__':
    app.run(debug=True)
