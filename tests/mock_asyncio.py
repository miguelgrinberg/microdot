try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

from tests import mock_socket


def get_event_loop():
    return asyncio.get_event_loop()


async def start_server(cb, host, port):
    class MockServer:
        def __init__(self):
            self.closed = False

        async def run(self):
            s = mock_socket.socket()
            while not self.closed:
                fd, addr = s.accept()
                fd = mock_socket.FakeStreamAsync(fd)
                await cb(fd, fd)

        def close(self):
            self.closed = True

        async def wait_closed(self):
            while not self.closed:
                await asyncio.sleep(0.01)

    server = MockServer()
    asyncio.get_event_loop().create_task(server.run())
    return server


def run(coro):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)
