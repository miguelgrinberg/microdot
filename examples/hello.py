from microdot import Microdot, Response

app = Microdot()

htmldoc = """<!DOCTYPE html>
<html>
    <head>
        <title>Microdot Example Page</title>
    </head>
    <body>
        <div>
            <h1>Microdot Example Page</h1>
            <p>Hello from Microdot!</p>
        </div>
    </body>
</html>
"""


@app.route("", methods=["GET", "POST"])
def serial_number(request):
    print(request.headers)
    return Response(body=htmldoc, headers={"Content-Type": "text/html"})


app.run(debug=True)
