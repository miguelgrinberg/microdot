try:
    import utime as time
except ImportError:
    import time

from microdot import Microdot

app = Microdot()

frames = []
for file in ['1.jpg', '2.jpg', '3.jpg']:
    with open(file, 'rb') as f:
        frames.append(f.read())


@app.route('/')
def index(request):
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
def video_feed(request):
    def stream():
        yield b'--frame\r\n'
        while True:
            for frame in frames:
                yield b'Content-Type: image/jpeg\r\n\r\n' + frame + \
                    b'\r\n--frame\r\n'
                time.sleep(1)

    return stream(), 200, {'Content-Type':
                           'multipart/x-mixed-replace; boundary=frame'}


if __name__ == '__main__':
    app.run(debug=True)
