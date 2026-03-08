from typing import Any, Awaitable, Callable
from microdot import *  # type: ignore
from microdot.microdot import Microdot as BaseMicrodot, Request
from microdot.websocket import WebSocket as BaseWebSocket

class Microdot(BaseMicrodot):  # type: ignore[no-redef]
    lifespan_startup: Callable[[dict[str, Any]], Awaitable[None]]
    lifespan_shutdown: Callable[[dict[str, Any]], Awaitable[None]]
    embedded_server: bool
    def __init__(self, lifespan_startup: Callable[[dict[str, Any]], Awaitable[None]] = ..., lifespan_shutdown: Callable[[dict[str, Any]], Awaitable[None]] = ...) -> None:
        ...
    
    async def handle_lifespan(self, scope: dict[str, Any], receive: Callable[[], Awaitable[dict[str, Any]]], send: Callable[[dict[str, Any], Awaitable[None]]]) -> None:
        ...
    
    async def asgi_app(self, scope: dict[str, Any], receive: Callable[[], Awaitable[dict[str, Any]]], send: Callable[[dict[str, Any], Awaitable[None]]]):
        ...
    
    async def __call__(self, scope: dict[str, Any], receive: Callable[[], Awaitable[dict[str, Any]]], send: Callable[[dict[str, Any], Awaitable[None]]]):
        ...
    
    def shutdown(self) -> None:
        ...
    
    def run(self, host: str = ..., port: int = ..., debug: bool = ..., **options: Any) -> None:  # type: ignore[override]
        ...
    


class WebSocket(BaseWebSocket):
    closed: bool
    async def handshake(self) -> None:
        ...
    
    async def receive(self) -> bytes | str:
        ...
    
    async def send(self, data: bytes | str) -> None:  # type: ignore[override]
        ...
    
    async def close(self) -> None:
        ...
    


async def websocket_upgrade(request: Request) -> BaseWebSocket:
    ...

def with_websocket(f: Callable[[Request, BaseWebSocket], Awaitable[None]]) -> None:
    ...
