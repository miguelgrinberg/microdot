API Reference
=============

``microdot`` module
-------------------

The ``microdot`` module defines a few classes that help implement HTTP-based
servers for MicroPython and standard Python, with multithreading support for
Python interpreters that support it.

``Microdot`` class
~~~~~~~~~~~~~~~~~~

.. autoclass:: microdot.Microdot
   :members:

``Request`` class
~~~~~~~~~~~~~~~~~

.. autoclass:: microdot.Request
   :members:

``Response`` class
~~~~~~~~~~~~~~~~~~

.. autoclass:: microdot.Response
   :members:

``MultiDict`` class
~~~~~~~~~~~~~~~~~~~

.. autoclass:: microdot.MultiDict
   :members:

``microdot_asyncio`` module
---------------------------

The ``microdot_asyncio`` module defines a few classes that help implement
HTTP-based servers for MicroPython and standard Python that use ``asyncio``
and coroutines.

``Microdot`` class
~~~~~~~~~~~~~~~~~~

.. autoclass:: microdot_asyncio.Microdot
   :inherited-members:
   :members:

``Request`` class
~~~~~~~~~~~~~~~~~

.. autoclass:: microdot_asyncio.Request
   :inherited-members:
   :members:

``Response`` class
~~~~~~~~~~~~~~~~~~

.. autoclass:: microdot_asyncio.Response
   :inherited-members:
   :members:

``microdot_wsgi`` module
------------------------

The ``microdot_wsgi`` module provides an extended ``Microdot`` class that
implements the WSGI protocol and can be used with a complaint WSGI web server
such as `Gunicorn <https://gunicorn.org/>`_ or
`uWSGI <https://uwsgi-docs.readthedocs.io/en/latest/>`_.

``Microdot`` class
~~~~~~~~~~~~~~~~~~

.. autoclass:: microdot_wsgi.Microdot
   :members:
   :exclude-members: shutdown, run

``microdot_asgi`` module
------------------------

The ``microdot_asgi`` module provides an extended ``Microdot`` class that
implements the ASGI protocol and can be used with a complaint ASGI server such
as `Uvicorn <https://www.uvicorn.org/>`_.

``Microdot`` class
~~~~~~~~~~~~~~~~~~

.. autoclass:: microdot_asgi.Microdot
   :members:
   :exclude-members: shutdown, run
