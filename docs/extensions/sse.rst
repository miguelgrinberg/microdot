Server-Sent Events
~~~~~~~~~~~~~~~~~~

.. list-table::
   :align: left

   * - Compatibility
     - | CPython & MicroPython

   * - Required Microdot source files
     -  | `sse.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/sse.py>`_
        | `helpers.py <https://github.com/miguelgrinberg/microdot/tree/main/src/microdot/helpers.py>`_

   * - Required external dependencies
     - | None

   * - Examples
     - | `counter.py <https://github.com/miguelgrinberg/microdot/blob/main/examples/sse/counter.py>`_

The Server-Sent Events (SSE) extension simplifies the creation of a streaming
endpoint that follows the SSE web standard. The :func:`with_sse <microdot.sse.with_sse>`
decorator is used to mark a route as an SSE handler. Decorated routes receive
an SSE object as second argument. The SSE object provides a ``send()``
asynchronous method to send an event to the client.

Example::

    from microdot.sse import with_sse

    @app.route('/events')
    @with_sse
    async def events(request, sse):
        for i in range(10):
            await asyncio.sleep(1)
            await sse.send({'counter': i})  # unnamed event
        await sse.send('end', event='comment')  # named event

To end the SSE connection, the route handler can exit, without returning
anything, as shown in the above examples.

If the client ends the SSE connection from their side, the route function is
cancelled. The route function can catch the ``CancelledError`` exception from
asyncio to perform cleanup tasks::

    @app.route('/events')
    @with_sse
    async def events(request, sse):
        try:
            i = 0
            while True:
                await asyncio.sleep(1)
                await sse.send({'counter': i})
                i += 1
        except asyncio.CancelledError:
            print('Client disconnected!')

.. note::
   The SSE protocol is unidirectional, so there is no ``receive()`` method in
   the SSE object. For bidirectional communication with the client, use the
   WebSocket extension.
