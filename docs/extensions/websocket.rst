WebSocket
~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     -  | `websocket.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/websocket.py>`_
        | `helpers.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/helpers.py>`_

   * - Required external dependencies
     - | None

   * - Examples
     - | `echo.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/websocket/echo.py>`_

The WebSocket extension gives the application the ability to handle WebSocket
requests. The :func:`with_websocket <microdot.websocket.with_websocket>`
decorator is used to mark a route handler as a WebSocket handler. Decorated
routes receive a WebSocket object as a second argument. The WebSocket object
provides ``send()`` and ``receive()`` asynchronous methods to send and receive
messages respectively.

Example::

    from microdot.websocket import with_websocket

    @app.route('/echo')
    @with_websocket
    async def echo(request, ws):
        while True:
            message = await ws.receive()
            await ws.send(message)

To end the WebSocket connection, the route handler can exit, without returning
anything::

    @app.route('/echo')
    @with_websocket
    async def echo(request, ws):
        while True:
            message = await ws.receive()
            if message == 'exit':
                break
            await ws.send(message)
        await ws.send('goodbye')

If the client ends the WebSocket connection from their side, the route function
is cancelled. The route function can catch the ``CancelledError`` exception
from asyncio to perform cleanup tasks::

    @app.route('/echo')
    @with_websocket
    async def echo(request, ws):
        try:
            while True:
                message = await ws.receive()
                await ws.send(message)
        except asyncio.CancelledError:
            print('Client disconnected!')
