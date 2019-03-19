import machine
from microdot import Microdot, redirect, send_file

app = Microdot()


@app.route('/', methods=['GET', 'POST'])
def index(request):
    if request.method == 'POST':
        if 'set-read' in request.form:
            pin = machine.Pin(int(request.form['pin']), machine.Pin.IN)
        else:
            pin = machine.Pin(int(request.form['pin']), machine.Pin.OUT)
            pin.value(0 if 'set-low' in request.form else 1)
        return redirect('/')
    return send_file('gpio.html')


app.run()
