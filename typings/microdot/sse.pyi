from typing import Any, Awaitable, Callable
from asyncio import Event
from microdot import Request

class SSE:
    event: Event
    queue: list[bytes]
    def __init__(self) -> None:
        ...
    
    async def send(self, data: str | bytes | dict[str, Any] | list[Any], event: str | None = ..., event_id: str | None = ..., retry: int | None = ..., comment: bool = ...) -> None:
        ...
    


def sse_response(request: Request, event_function: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any):
    ...

def with_sse(f: Callable[..., Any]) -> Callable[..., Any]:
    ...
