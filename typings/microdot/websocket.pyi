from typing import Any, Awaitable, Callable
from microdot import Request

class WebSocketError(Exception):
    ...


class WebSocket:
    CONT: int
    TEXT: int
    BINARY: int
    CLOSE: int
    PING: int
    PONG: int
    max_message_length: int
    request: Request
    closed: bool
    def __init__(self, request: Request) -> None:
        ...
    
    async def handshake(self) -> None:
        ...
    
    async def receive(self) -> str | bytes:
        ...
    
    async def send(self, data: str | bytes, opcode: int | None = ...) -> None:
        ...
    
    async def close(self) -> None:
        ...
    


async def websocket_upgrade(request: Request) -> WebSocket:
    ...

def websocket_wrapper(f, upgrade_function: Callable[[Request], Awaitable[WebSocket]]):
    ...

def with_websocket(f: Callable[..., Any]) -> Callable[..., Any]:
    ...
