# SPDX-FileCopyrightText: 2019-2020 Damien P. George
#
# SPDX-License-Identifier: MIT
#
# MicroPython uasyncio module
# MIT license; Copyright (c) 2019-2020 Damien P. George
#
# This code comes from MicroPython, and has not been run through black or pylint there.
# Altering these files significantly would make merging difficult, so we will not use
# pylint or black.
# pylint: skip-file
# fmt: off
"""
Streams
=======
"""

from . import core


class Stream:
    """This represents a TCP stream connection. To minimise code this class
    implements both a reader and a writer, and both ``StreamReader`` and
    ``StreamWriter`` alias to this class.
    """

    def __init__(self, s, e={}):
        self.s = s
        self.e = e
        self.out_buf = b""

    def get_extra_info(self, v):
        """Get extra information about the stream, given by *v*. The valid
        values for *v* are: ``peername``.
        """

        return self.e[v]

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    def close(self):
        pass

    async def wait_closed(self):
        """Wait for the stream to close.

        This is a coroutine.
        """

        # TODO yield?
        self.s.close()

    async def read(self, n):
        """Read up to *n* bytes and return them.

        This is a coroutine.
        """

        await core._io_queue.queue_read(self.s)
        return self.s.read(n)

    async def readinto(self, buf):
        """Read up to n bytes into *buf* with n being equal to the length of *buf*

        Return the number of bytes read into *buf*

        This is a coroutine, and a MicroPython extension.
        """

        await core._io_queue.queue_read(self.s)
        return self.s.readinto(buf)

    async def readexactly(self, n):
        """Read exactly *n* bytes and return them as a bytes object.

        Raises an ``EOFError`` exception if the stream ends before reading
        *n* bytes.

        This is a coroutine.
        """

        r = b""
        while n:
            await core._io_queue.queue_read(self.s)
            r2 = self.s.read(n)
            if r2 is not None:
                if not len(r2):
                    raise EOFError
                r += r2
                n -= len(r2)
        return r

    async def readline(self):
        """Read a line and return it.

        This is a coroutine.
        """

        l = b""
        while True:
            await core._io_queue.queue_read(self.s)
            l2 = self.s.readline()  # may do multiple reads but won't block
            l += l2
            if not l2 or l[-1] == 10:  # \n (check l in case l2 is str)
                return l

    def write(self, buf):
        """Accumulated *buf* to the output buffer. The data is only flushed when
        `Stream.drain` is called. It is recommended to call `Stream.drain`
        immediately after calling this function.
        """
        if not self.out_buf:
            # Try to write immediately to the underlying stream.
            ret = self.s.write(buf)
            if ret == len(buf):
                return
            if ret is not None:
                buf = buf[ret:]

        self.out_buf += buf

    async def drain(self):
        """Drain (write) all buffered output data out to the stream.

        This is a coroutine.
        """

        mv = memoryview(self.out_buf)
        off = 0
        while off < len(mv):
            await core._io_queue.queue_write(self.s)
            ret = self.s.write(mv[off:])
            if ret is not None:
                off += ret
        self.out_buf = b""


# Stream can be used for both reading and writing to save code size
StreamReader = Stream
StreamWriter = Stream


# Create a TCP stream connection to a remote host
async def open_connection(host, port):
    """Open a TCP connection to the given *host* and *port*. The *host* address will
    be resolved using `socket.getaddrinfo`, which is currently a blocking call.

    Returns a pair of streams: a reader and a writer stream. Will raise a socket-specific
    ``OSError`` if the host could not be resolved or if the connection could not be made.

    This is a coroutine.
    """

    from uerrno import EINPROGRESS
    import usocket as socket

    ai = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)[0]  # TODO this is blocking!
    s = socket.socket(ai[0], ai[1], ai[2])
    s.setblocking(False)
    ss = Stream(s)
    try:
        s.connect(ai[-1])
    except OSError as er:
        if er.errno != EINPROGRESS:
            raise er
    await core._io_queue.queue_write(s)
    return ss, ss


# Class representing a TCP stream server, can be closed and used in "async with"
class Server:
    """This represents the server class returned from `start_server`.  It can be used in
    an ``async with`` statement to close the server upon exit.
    """

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.close()
        await self.wait_closed()

    def close(self):
        """Close the server."""

        self.task.cancel()

    async def wait_closed(self):
        """Wait for the server to close.

        This is a coroutine.
        """

        await self.task

    async def _serve(self, s, cb):
        # Accept incoming connections
        while True:
            try:
                await core._io_queue.queue_read(s)
            except core.CancelledError:
                # Shutdown server
                s.close()
                return
            try:
                s2, addr = s.accept()
            except:
                # Ignore a failed accept
                continue
            s2.setblocking(False)
            s2s = Stream(s2, {"peername": addr})
            core.create_task(cb(s2s, s2s))


# Helper function to start a TCP stream server, running as a new task
# TODO could use an accept-callback on socket read activity instead of creating a task
async def start_server(cb, host, port, backlog=5):
    """Start a TCP server on the given *host* and *port*. The *cb* callback will be
    called with incoming, accepted connections, and be passed 2 arguments: reader
    writer streams for the connection.

    Returns a `Server` object.

    This is a coroutine.
    """

    import usocket as socket

    # Create and bind server socket.
    host = socket.getaddrinfo(host, port)[0]  # TODO this is blocking!
    s = socket.socket()
    s.setblocking(False)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(host[-1])
    s.listen(backlog)

    # Create and return server object and task.
    srv = Server()
    srv.task = core.create_task(srv._serve(s, cb))
    return srv


################################################################################
# Legacy uasyncio compatibility


async def stream_awrite(self, buf, off=0, sz=-1):
    if off != 0 or sz != -1:
        buf = memoryview(buf)
        if sz == -1:
            sz = len(buf)
        buf = buf[off : off + sz]
    self.write(buf)
    await self.drain()


Stream.aclose = Stream.wait_closed
Stream.awrite = stream_awrite
Stream.awritestr = stream_awrite  # TODO explicitly convert to bytes?
