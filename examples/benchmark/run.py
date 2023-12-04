import os
import subprocess
import time
from timeit import timeit
import requests
import psutil
import humanize

apps = [
    (
        ['micropython', '-c', 'import time; time.sleep(10)'],
        {},
        'baseline-micropython'
    ),
    (
        'micropython mem.py',
        {'MICROPYPATH': '../../src:../../libs/micropython'},
        'microdot-micropython'
    ),
    (
        ['python', '-c', 'import time; time.sleep(10)'],
        {},
        'baseline-python'
    ),
    (
        'python mem.py',
        {'PYTHONPATH': '../../src'},
        'microdot-cpython'
    ),
    (
        'uvicorn --workers 1 --port 5000 mem_asgi:app',
        {'PYTHONPATH': '../../src'},
        'microdot-uvicorn'
    ),
    (
        'gunicorn --workers 1 --bind :5000 mem_wsgi:app',
        {'PYTHONPATH': '../../src'},
        'microdot-gunicorn'
    ),
    (
        'flask run',
        {'FLASK_APP': 'mem_flask.py'},
        'flask-run'
    ),
    (
        'quart run',
        {'QUART_APP': 'mem_quart.py'},
        'quart-run'
    ),
    (
        'gunicorn --workers 1 --bind :5000 mem_flask:app',
        {},
        'flask-gunicorn'
    ),
    (
        'uvicorn --workers 1 --port 5000 mem_quart:app',
        {},
        'quart-uvicorn'
    ),
    (
        'uvicorn --workers 1 --port 5000 mem_fastapi:app',
        {},
        'fastapi-uvicorn'
    ),
]

for app, env, name in apps:
    p = subprocess.Popen(
        app.split() if isinstance(app, str) else app,
        env={'PATH': os.environ['PATH'] + ':../../bin', **env},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(1)
    tm = 0
    if not name.startswith('baseline'):
        def req():
            r = requests.get('http://localhost:5000')
            r.raise_for_status()

        tm = timeit(req, number=1000)
    proc = psutil.Process(p.pid)
    mem = proc.memory_info().rss
    for child in proc.children(recursive=True):
        mem += child.memory_info().rss
    bar = '*' * (mem // (1024 * 1024))
    print(f'{name:<28}{tm:10.2f}s {humanize.naturalsize(mem):>10} {bar}')
    p.terminate()
    time.sleep(1)
