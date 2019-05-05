try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

from tests import mock_socket

_calls = []


class EventLoop:
    def run_until_complete(self, coro):
        _calls.append(('run_until_complete', coro))
        self.coro = coro

    def run_forever(self):
        _calls.append(('run_forever',))

        async def rf():
            s = mock_socket.socket()
            while True:
                fd, addr = s.accept()
                fd = mock_socket.FakeStreamAsync(fd)
                await self.coro(fd, fd)

        asyncio.get_event_loop().run_until_complete(rf())

    def close(self):
        pass


loop = EventLoop()


def get_event_loop():
    _calls.append(('get_event_loop',))
    return loop


def start_server(cb, host, port):
    _calls.append(('start_server', cb, host, port))
    return cb
