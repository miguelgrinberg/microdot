Core Extensions
---------------

Microdot is a highly extensible web application framework. The extensions
described in this section are maintained as part of the Microdot project and
can be obtained from the same source code repository.

Asynchronous Support with ``asyncio``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_asyncio.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_asyncio.py>`_

   * - Required external dependencies
     - | CPython: None
       | MicroPython: `uasyncio <https://github.com/micropython/micropython/tree/master/extmod/uasyncio>`_

Microdot can be extended to use an asynchronous programming model based on the
``asyncio`` package. When the :class:`Microdot <microdot_asyncio.Microdot>`
class is imported from the ``microdot_asyncio`` package, an asynchronous server
is used.

The example that follows uses ``asyncio`` coroutines for concurrency::

    from microdot_asyncio import Microdot

    app = Microdot()

    @app.route('/')
    async def hello(request):
        return 'Hello, world!'

    app.run()

Rendering HTML Templates
~~~~~~~~~~~~~~~~~~~~~~~~

Using the uTemplate Engine
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_utemplate.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_utemplate.py>`_

   * - Required external dependencies
     - | `utemplate <https://github.com/pfalcon/utemplate/tree/master/utemplate>`_

Using the Jinja Engine
^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :align: left

   * - Compatibility
     - | CPython only

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_jinja.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_jinja.py>`_

   * - Required external dependencies
     - | `Jinja2 <https://jinja.palletsprojects.com/>`_

Maintaing Secure User Sessions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_session.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_session.py>`_

   * - Required external dependencies
     - | CPython: `PyJWT <https://pyjwt.readthedocs.io/>`_
       | MicroPython: `ujwt.py <https://github.com/miguelgrinberg/micropython-lib/blob/ujwt-module/python-ecosys/ujwt/ujwt.py>`_,
                      `hmac <https://github.com/micropython/micropython-lib/blob/master/python-stdlib/hmac/hmac.py>`_,
                      `hashlib <https://github.com/miguelgrinberg/micropython-lib/blob/ujwt-module/python-stdlib/hashlib>`_,
                      `warnings <https://github.com/micropython/micropython-lib/blob/master/python-stdlib/warnings/warnings.py>`_

Test Client
~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_test_client.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_test_client.py>`_

   * - Required external dependencies
     - | None

Deploying on a Production Web Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using a WSGI Web Server
^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :align: left

   * - Compatibility
     - | CPython only

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_wsgi.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_wsgi.py>`_

   * - Required external dependencies
     - | A WSGI web server, such as `Gunicorn <https://gunicorn.org/>`_.

Using an ASGI Web Server
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :align: left

   * - Compatibility
     - | CPython only

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot.py>`_
       | `microdot_asyncio.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_asyncio.py>`_
       | `microdot_asgi.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot_asgi.py>`_

   * - Required external dependencies
     - | An ASGI web server, such as `Uvicorn <https://uvicorn.org/>`_.

