from typing import Any, Callable
from microdot import Microdot, Request

class SessionDict(dict):
    request: Request
    def __init__(self, request: Request, session_dict: dict[str, Any]) -> None:
        ...
    
    def save(self) -> None:
        ...
    
    def delete(self) -> None:
        ...
    


class Session:
    secret_key: str | bytes
    cookie_options: dict[str, Any]
    def __init__(self, app: Microdot | None = ..., secret_key: str | bytes | None = ..., cookie_options: dict[str, Any] | None = ...) -> None:
        ...
    
    def initialize(self, app: Microdot, secret_key: str | bytes | None = ..., cookie_options: dict[str, Any] | None = ...) -> None:
        ...
    
    def get(self, request: Request) -> SessionDict:
        ...
    
    def update(self, request: Request, session: dict[str, Any]) -> None:
        ...
    
    def delete(self, request: Request) -> None:
        ...
    
    def encode(self, payload: dict[str, Any], secret_key: str | bytes | None = ...) -> str:
        ...
    
    def decode(self, session: str, secret_key: str | bytes | None = ...) -> dict[str, Any]:
        ...
    


def with_session(f: Callable[..., Any]) -> Callable[..., Any]:
    ...

