Concurrency
~~~~~~~~~~~

Microdot implements concurrency through the ``asyncio`` package, which means
that applications must be careful to prevent blocking in their handlers.

"async def" handlers
^^^^^^^^^^^^^^^^^^^^

The recommendation for route handlers in Microdot is to use asynchronous
functions, declared as ``async def``. Microdot executes these handler
functions as native asynchronous tasks. The standard considerations for writing
asynchronous code apply, and in particular blocking calls should be avoided to
ensure the application runs smoothly and is always responsive.

"def" handlers
^^^^^^^^^^^^^^

Microdot also supports the use of synchronous route handlers, declared as
standard ``def`` functions. These handlers are handled differently under
CPython and MicroPython.

When running on CPython, Microdot executes synchronous handlers in a
`thread executor <https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor>`_,
which uses a thread pool. The use of blocking or CPU intensive code in these
handlers does not have such a negative effect on the application, because
handlers do not run on the same thread as the asynchronous loop. On the other
hand, the application will be affected by threading issues such as those caused
by the Global Interpreter Lock.

Under MicroPython the situation is different. Most microcontroller boards
do not have or have very limited threading support, so Microdot executes
synchronous handlers in the main and often only thread available. This means
that these functions will block the asynchronous loop when they take too long
to complete. The use of properly written asynchronous handlers should be
preferred.
