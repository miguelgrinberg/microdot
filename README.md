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

- [Change Log](https://github.com/miguelgrinberg/microdot/blob/main/CHANGES.md)
- Documentation
    - [Latest](https://microdot.readthedocs.io/en/latest/)
    - [Stable (v2)](https://microdot.readthedocs.io/en/stable/)
    - [Legacy (v1)](https://microdot.readthedocs.io/en/v1/) ([Code](https://github.com/miguelgrinberg/microdot/tree/v1))

## Roadmap

The following features are planned for future releases of Microdot, both for
MicroPython and CPython:

- Authentication support, similar to [Flask-Login](https://github.com/maxcountryman/flask-login) for Flask (**Added in version 2.1**)
- Support for forms encoded in `multipart/form-data` format (**Added in version 2.2**)
- OpenAPI integration, similar to [APIFairy](https://github.com/miguelgrinberg/apifairy) for Flask

In addition to the above, the following extensions are also under consideration,
but only for CPython:

- Database integration through [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)
- Socket.IO support through [python-socketio](https://github.com/miguelgrinberg/python-socketio)

Do you have other ideas to propose? Let's [discuss them](https://github.com/:miguelgrinberg/microdot/discussions/new?category=ideas)!
