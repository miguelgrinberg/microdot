import asyncio
import dht
import gc
import machine
import network
import socket
import time

import config
from microdot import Microdot, send_file

app = Microdot()
current_temperature = None
current_humidity = None
current_time = None


def wifi_connect():
    """Connect to the configured Wi-Fi network.
    Returns the IP address of the connected interface.
    """
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config.WIFI_ESSID, config.WIFI_PASSWORD)
        for i in range(20):
            if sta_if.isconnected():
                break
            time.sleep(1)
        if not sta_if.isconnected():
            raise RuntimeError('Could not connect to network')
    return sta_if.ifconfig()[0]


def get_current_time():
    """Return the current Unix time.
    Note that because many microcontrollers do not have a clock, this function
    makes a call to an NTP server to obtain the current time. A Wi-Fi
    connection needs to be in place before calling this function.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)
    s.sendto(b'\x1b' + 47 * b'\0',
             socket.getaddrinfo('pool.ntp.org', 123)[0][4])
    msg, _ = s.recvfrom(1024)
    return ((msg[40] << 24) | (msg[41] << 16) | (msg[42] << 8) | msg[43]) - \
        2208988800


def get_current_weather():
    """Read the temperature and humidity from the DHT22 sensor.
    Returns them as a tuple. The returned temperature is in degrees Celcius.
    The humidity is a 0-100 percentage.
    """
    d = dht.DHT22(machine.Pin(config.DHT22_PIN))
    d.measure()
    return d.temperature(), d.humidity()


async def refresh_weather():
    """Background task that updates the temperature and humidity.
    This task is designed to run in the background. It connects to the DHT22
    temperature and humidity sensor once per minute and stores the updated
    readings in global variables.
    """
    global current_temperature
    global current_humidity
    global current_time

    while True:
        try:
            t = get_current_time()
            temp, hum = get_current_weather()
        except asyncio.CancelledError:
            raise
        except Exception as error:
            print(f'Could not obtain weather, error: {error}')
        else:
            current_time = t
            current_temperature = int(temp * 10) / 10
            current_humidity = int(hum * 10) / 10
        gc.collect()
        await asyncio.sleep(60)


@app.route('/')
async def index(request):
    return send_file('index.html')


@app.route('/api')
async def api(request):
    return {
        'temperature': current_temperature,
        'humidity': current_humidity,
        'time': current_time,
    }


async def start():
    ip = wifi_connect()
    print(f'Starting server at http://{ip}:8000...')
    bgtask = asyncio.create_task(refresh_weather())
    server = asyncio.create_task(app.start_server(port=8000))
    await asyncio.gather(server, bgtask)


asyncio.run(start())
