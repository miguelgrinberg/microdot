# microdot
[![Build status](https://github.com/miguelgrinberg/microdot/workflows/build/badge.svg)](https://github.com/miguelgrinberg/microdot/actions) [![codecov](https://codecov.io/gh/miguelgrinberg/microdot/branch/main/graph/badge.svg)](https://codecov.io/gh/miguelgrinberg/microdot)

*“The impossibly small web framework for Python and MicroPython”*

Microdot is a minimalistic Python web framework inspired by Flask, and designed
to run on systems with limited resources such as microcontrollers. It runs on
standard Python and on MicroPython.

```python
from microdot import Microdot

app = Microdot()

@app.route('/')
def index(request):
    return 'Hello, world!'

app.run()
```

## Resources

- [Documentation](https://microdot.readthedocs.io/en/latest/)
- [Change Log](https://github.com/miguelgrinberg/microdot/blob/main/CHANGES.md)
