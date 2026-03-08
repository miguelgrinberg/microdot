from typing import Any, AsyncGenerator, Generator, Tuple
from asyncio import StreamReader, StreamWriter
from microdot import Microdot, Response

__all__ = ['TestClient', 'TestResponse']
class TestResponse:
    status_code: int
    reason: str
    headers: dict[str, str]
    body: bytes
    text: str
    json: dict[str, Any] | list[Any]
    events: list[dict[str, Any]]
    def __init__(self) -> None:
        ...
    
    @classmethod
    async def create(cls, res: Response):
        ...
    


class TestClient:
    __test__: bool
    app: Microdot
    cookies: dict[str, str]
    scheme: str
    host: str
    def __init__(self, app: Microdot, cookies: dict[str, str] | None = ..., scheme: str | None = ..., host: str | None = ...) -> None:
        ...
    
    async def request(self, method: str, path: str, headers: dict[str, str] | None = ..., body: bytes | None = ..., sock: Tuple[StreamReader, StreamWriter] | None = ...):
        ...
    
    async def get(self, path: str, headers: dict[str, str] | None = ...):
        ...
    
    async def post(self, path: str, headers: dict[str, str] | None = ..., body=...):
        ...
    
    async def put(self, path: str, headers: dict[str, str] | None = ..., body=...):
        ...
    
    async def patch(self, path: str, headers: dict[str, str] | None = ..., body=...):
        ...
    
    async def delete(self, path: str, headers: dict[str, str] | None = ...):
        ...
    
    async def websocket(self, path: str, client: Generator[str | bytes, None, None] | AsyncGenerator[str | bytes, None], headers: dict[str, str] | None = ...):
        ...
