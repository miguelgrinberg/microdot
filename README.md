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

## Resources

- [Change Log](https://github.com/miguelgrinberg/microdot/blob/main/CHANGES.md)
- Documentation
    - [Latest](https://microdot.readthedocs.io/en/latest/)
    - [Stable (v2)](https://microdot.readthedocs.io/en/stable/)

The following links are for version 1 of Microdot:

- [Code](https://github.com/miguelgrinberg/microdot/tree/v1)
- [Documentation](https://microdot.readthedocs.io/en/v1/)

Note that version 1 is no longer maintained, so you should consider migrating
to version 2. See the
[migration notes](https://microdot.readthedocs.io/en/latest/implementation/migrating.html)
for help.

## Roadmap

The following features are planned for future releases of Microdot, both for
MicroPython and CPython:

- Authentication support, similar to [Flask-Login](https://github.com/maxcountryman/flask-login) for Flask (**Added in version 2.1**)
- Support for forms encoded in `multipart/form-data` format (**Added in version 2.2**)
- CSRF protection extension (**Added in version 2.5**)
- Pub/sub mini-framework for WebSocket and SSE
- OpenAPI integration, similar to [APIFairy](https://github.com/miguelgrinberg/apifairy) for Flask

Do you have other ideas to propose? Let's [discuss them](https://github.com/:miguelgrinberg/microdot/discussions/new?category=ideas)!
