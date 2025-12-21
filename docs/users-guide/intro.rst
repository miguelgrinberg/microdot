Introduction
~~~~~~~~~~~~

This section covers how to create and run a basic Microdot web application.

A simple web server
^^^^^^^^^^^^^^^^^^^

The following is an example of a simple web server::

    from microdot import Microdot

    app = Microdot()

    @app.route('/')
    async def index(request):
        return 'Hello, world!'

    app.run()

The script imports the :class:`Microdot <microdot.Microdot>` class and creates
an application instance from it.

The application instance provides a :func:`route() <microdot.Microdot.route>`
decorator, which is used to define one or more routes, as needed by the
application.

The ``route()`` decorator takes the path portion of the URL as an
argument, and maps it to the decorated function, so that the function is called
when the client requests the URL.

When the function is called, it is passed a :class:`Request <microdot.Request>`
object as an argument, which provides access to the information passed by the
client. The value returned by the function is sent back to the client as the
response.

Microdot is an asynchronous framework that uses the ``asyncio`` package. Route
handler functions can be defined as ``async def`` or ``def`` functions, but
``async def`` functions are recommended for performance.

The :func:`run() <microdot.Microdot.run>` method starts the application's web
server on port 5000 by default, and creates its own asynchronous loop. This
method blocks while it waits for connections from clients.

For some applications it may be necessary to run the web server alongside other
asynchronous tasks, on an already running loop. In that case, instead of
``app.run()`` the web server can be started by invoking the
:func:`start_server() <microdot.Microdot.start_server>` coroutine as shown in
the following example::

    import asyncio
    from microdot import Microdot

    app = Microdot()

    @app.route('/')
    async def index(request):
        return 'Hello, world!'

    async def main():
        # start the server in a background task
        server = asyncio.create_task(app.start_server())

        # ... do other asynchronous work here ...

        # cleanup before ending the application
        await server

    asyncio.run(main())

Running with CPython
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :align: left

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/blob/main/src/microdot/microdot.py>`_

   * - Required external dependencies
     - | None

   * - Examples
     - | `hello.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/hello/hello.py>`_

When using CPython, you can start the web server by running the script that
has the ``app.run()`` call at the bottom::

    python main.py

After starting the script, open a web browser and navigate to
*http://localhost:5000/* to access the application at the default address for
the Microdot web server. From other computers in the same network, use the IP
address or hostname of the computer running the script instead of
``localhost``.

Running with MicroPython
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :align: left

   * - Required Microdot source files
     - | `microdot.py <https://github.com/miguelgrinberg/microdot/blob/main/src/microdot/microdot.py>`_

   * - Required external dependencies
     - | None

   * - Examples
     - | `hello.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/hello/hello.py>`_
       | `gpio.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/gpio/gpio.py>`_

When using MicroPython, you can upload a *main.py* file containing the web
server code to your device, along with the required Microdot files, as defined
in the :ref:`MicroPython Installation` section.

MicroPython will automatically run *main.py* when the device is powered on, so
the web server will automatically start. The application can be accessed on
port 5000 at the device's IP address. As indicated above, the port can be
changed by passing the ``port`` argument to the ``run()`` method.

.. note::
   Microdot does not configure the network interface of the device in which it
   is running. If your device requires a network connection to be made in
   advance, for example to a Wi-Fi access point, this must be configured before
   the ``run()`` method is invoked.

Web Server Configuration
^^^^^^^^^^^^^^^^^^^^^^^^

The :func:`run() <microdot.Microdot.run>` and
:func:`start_server() <microdot.Microdot.start_server>` methods support a few
arguments to configure the web server.

- ``port``: The port number to listen on. Pass the desired port number in this
  argument to use a port different than the default of 5000. For example::

    app.run(port=6000)

- ``host``: The IP address of the network interface to listen on. By default
  the server listens on all available interfaces. To listen only on the local
  loopback interface, pass ``'127.0.0.1'`` as value for this argument.
- ``debug``: when set to ``True``, the server ouputs logging information to the
  console. The default is ``False``.
- ``ssl``: an ``SSLContext`` instance that configures the server to use TLS
  encryption, or ``None`` to disable TLS use. The default is ``None``. The
  following example demonstrates how to configure the server with an SSL
  certificate stored in *cert.pem* and *key.pem* files::

    import ssl

    # ...

    sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslctx.load_cert_chain('cert.pem', 'key.pem')
    app.run(port=4443, debug=True, ssl=sslctx)

.. note::
   When using CPython, the certificate and key files must be given in PEM
   format. When using MicroPython, these files must be given in DER format.
