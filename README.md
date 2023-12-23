# microdot
[![Build status](https://github.com/miguelgrinberg/microdot/workflows/build/badge.svg)](https://github.com/miguelgrinberg/microdot/actions) [![codecov](https://codecov.io/gh/miguelgrinberg/microdot/branch/main/graph/badge.svg)](https://codecov.io/gh/miguelgrinberg/microdot)

*“The impossibly small web framework for Python and MicroPython”*

Microdot is a minimalistic Python web framework inspired by Flask. Given its
small size, it can run on systems with limited resources such as
microcontrollers. Both standard Python (CPython) and MicroPython are supported.

```python
from microdot import Microdot

app = Microdot()

@app.route('/')
async def index(request):
    return 'Hello, world!'

app.run()
```

## Migrating to Microdot 2

Version 2 of Microdot incorporates feedback received from users of earlier
releases, and attempts to improve and correct some design decisions that have
proven to be problematic.

For this reason most applications built for earlier versions will need to be
updated to work correctly with Microdot 2. The
[Migration Guide](https://microdot.readthedocs.io/en/stable/migrating.html)
describes the backwards incompatible changes that were made.

## Resources

- Documentation
    - [Stable](https://microdot.readthedocs.io/en/stable/)
    - [Latest](https://microdot.readthedocs.io/en/latest/)
- Still using version 1?
    - [Code](https://github.com/miguelgrinberg/microdot/tree/v1)
    - [Documentation](https://microdot.readthedocs.io/en/v1/)
- [Change Log](https://github.com/miguelgrinberg/microdot/blob/main/CHANGES.md)
