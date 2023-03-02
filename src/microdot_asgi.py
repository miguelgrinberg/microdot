import asyncio
import os
import signal
from microdot_asyncio import *  # noqa: F401, F403
from microdot_asyncio import Microdot as BaseMicrodot
from microdot_asyncio import Request
from microdot import NoCaseDict


class _BodyStream:  # pragma: no cover
    def __init__(self, receive):
        self.receive = receive
        self.data = b''
        self.more = True

    async def read_more(self):
        if self.more:
            packet = await self.receive()
            self.data += packet.get('body', b'')
            self.more = packet.get('more_body', False)

    async def read(self, n=-1):
        while self.more and len(self.data) < n:
            self.read_more()
        if len(self.data) < n:
            data = self.data
            self.data = b''
            return data

        data = self.data[:n]
        self.data = self.data[n:]
        return data

    async def readline(self):
        return self.readuntil()

    async def readexactly(self, n):
        return self.read(n)

    async def readuntil(self, separator=b'\n'):
        if self.more and separator not in self.data:
            self.read_more()
        data, self.data = self.data.split(separator, 1)
        return data


class Microdot(BaseMicrodot):
    def __init__(self):
        super().__init__()
        self.embedded_server = False

    async def asgi_app(self, scope, receive, send):
        """An ASGI application."""
        if scope['type'] not in ['http', 'websocket']:  # pragma: no cover
            return
        path = scope['path']
        if 'query_string' in scope and scope['query_string']:
            path += '?' + scope['query_string'].decode()
        headers = NoCaseDict()
        content_length = 0
        for key, value in scope.get('headers', []):
            headers[key] = value
            if key.lower() == 'content-length':
                content_length = int(value)

        if content_length and content_length <= Request.max_body_length:
            body = b''
            more = True
            while more:
                packet = await receive()
                body += packet.get('body', b'')
                more = packet.get('more_body', False)
            stream = None
        else:
            body = b''
            stream = _BodyStream(receive)

        req = Request(
            self,
            (scope['client'][0], scope['client'][1]),
            scope.get('method', 'GET'),
            path,
            'HTTP/' + scope['http_version'],
            headers,
            body=body,
            stream=stream,
            sock=(receive, send))
        req.asgi_scope = scope

        res = await self.dispatch_request(req)
        res.complete()

        header_list = []
        for name, value in res.headers.items():
            if not isinstance(value, list):
                header_list.append((name.lower().encode(), value.encode()))
            else:
                for v in value:
                    header_list.append((name.lower().encode(), v.encode()))

        if scope['type'] != 'http':  # pragma: no cover
            return

        await send({'type': 'http.response.start',
                    'status': res.status_code,
                    'headers': header_list})

        cancelled = False

        async def cancel_monitor():
            nonlocal cancelled

            while True:
                event = await receive()
                if event['type'] == 'http.disconnect':  # pragma: no branch
                    cancelled = True
                    break

        asyncio.ensure_future(cancel_monitor())

        body_iter = res.body_iter().__aiter__()
        try:
            body = await body_iter.__anext__()
            while not cancelled:  # pragma: no branch
                next_body = await body_iter.__anext__()
                await send({'type': 'http.response.body',
                            'body': body,
                            'more_body': True})
                body = next_body
        except StopAsyncIteration:
            await send({'type': 'http.response.body',
                        'body': body,
                        'more_body': False})

    async def __call__(self, scope, receive, send):
        return await self.asgi_app(scope, receive, send)

    def shutdown(self):
        if self.embedded_server:  # pragma: no cover
            super().shutdown()
        else:
            pid = os.getpgrp() if hasattr(os, 'getpgrp') else os.getpid()
            os.kill(pid, signal.SIGTERM)

    def run(self, host='0.0.0.0', port=5000, debug=False,
            **options):  # pragma: no cover
        """Normally you would not start the server by invoking this method.
        Instead, start your chosen ASGI web server and pass the ``Microdot``
        instance as the ASGI application.
        """
        self.embedded_server = True
        super().run(host=host, port=port, debug=debug, **options)
