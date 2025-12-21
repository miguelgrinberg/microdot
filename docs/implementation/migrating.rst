Migrating to Microdot 2.x from Older Releases
---------------------------------------------

Version 2 of Microdot incorporates feedback received from users of earlier
releases, and attempts to improve and correct some design decisions that have
proven to be problematic.

For this reason most applications built for earlier versions will need to be
updated to work correctly with Microdot 2. This section describes the backwards
incompatible changes that were made.

Code reorganization
~~~~~~~~~~~~~~~~~~~

The Microdot source code has been moved into a ``microdot`` package,
eliminating the need for each extension to be named with a *microdot_* prefix.

As a result of this change, all extensions have been renamed to shorter names.
For example, the *microdot_cors.py* module is now called *cors.py*.

This change affects the way extensions are imported. Instead of this::

    from microdot_cors import CORS

the import statement should be::

    from microdot.cors import CORS

No more synchronous web server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In earlier releases of Microdot the core web server was built on synchronous
Python, and asynchronous support was enabled with the asyncio extension.

Microdot 2 eliminates the synchronous web server, and implements the core
server logic directly with asyncio, eliminating the need for an asyncio
extension.

Any applications built using the asyncio extension will need to update their
imports from this::

    from microdot_asyncio import Microdot

to this::

    from microdot import Microdot

Applications that were built using the synchronous web server do not need to
change their imports, but will now work asynchronously. Review the
:ref:`Concurrency` section to learn about the potential issues when using
``def`` function handlers, and the benefits of transitioning to ``async def``
handlers.

Removed extensions
~~~~~~~~~~~~~~~~~~

Some extensions became unnecessary and have been removed or merged with other
extensions:

- *microdot_asyncio.py*: this is now the core web server.
- *microdot_asyncio_websocket.py*: this is now the main WebSocket extension.
- *microdot_asyncio_test_client.py*: this is now the main test client
  extension.
- *microdot_asgi_websocket.py*: the functionality in this extension is now
  available in the ASGI extension.
- *microdot_ssl.py*: this extension was only used with the synchronous web
  server, so it is not needed anymore.
- *microdot_websocket_alt.py*: this extension was only used with the
  synchronous web server, so it is not needed anymore.

No more ``render_template()`` function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Jinja and uTemplate extensions have been redesigned to work better under
the asynchronous engine, and as a result, the ``render_template()`` function
has been eliminated.

Instead of this::

    return render_template('index.html', title='Home')

use this::

    return Template('index.html').render(title='Home')

As a result of this change, it is now possible to use asynchronous rendering::

    return await Template('index.html').render_async(title='Home')

Also thanks to this redesign, the template can be streamed instead of returned
as a single string::

    return Template('index.html').generate(title='Home')

Streamed templates also have an asynchronous version::

    return Template('index.html').generate_async(title='Home')

Class-based user sessions
~~~~~~~~~~~~~~~~~~~~~~~~~

The session extension has been completely redesigned. To initialize session
support for the application, create a ``Session`` object::

    app = Microdot()
    Session(app, secret_key='top-secret!')

The ``@with_session`` decorator is used to include the session in a request::

    @app.get('/')
    @with_session
    async def index(request, session):
        # ...

The ``session`` can be used as a dictionary to retrieve or change the session.
To save the session when it has been modified, call its ``save()`` method::

    @app.get('/')
    @with_session
    async def index(request, session):
        # ...
        session.save()
        return 'OK'

To delete the session, call its ``delete()`` method before returning from the
request.

WSGI extension redesign
~~~~~~~~~~~~~~~~~~~~~~~

Given that the synchronous web server has been removed, the WSGI extension has
been redesigned to work as a synchronous wrapper for the asynchronous web
server.

Applications using the WSGI extension continue to run under an asynchronous
loop and should try to use the recommended ``async def`` handlers, but can be
deployed with standard WSGI servers such as Gunicorn.

WebSocket support when using the WSGI extension is enabled when using a
compatible web server. At this time only Gunicorn is supported for WebSocket.
Given that WebSocket support is asynchronous, it would be better to switch to
the ASGI extension, which has full support for WebSocket as defined in the ASGI
specification.

As before, the WSGI extension is not available under MicroPython.
