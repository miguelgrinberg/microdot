from typing import Any, Awaitable, Callable
from microdot import Request, Response

class Login:
    login_url: str
    user_loader_callback: Callable[[str], Any | Awaitable[Any]]
    def __init__(self, login_url: str = ...) -> None:
        ...
    
    def user_loader(self, f: Callable[[str], Any | Awaitable[Any]]) -> None:
        ...
    
    async def login_user(self, request: Request, user: Any, remember: bool = ..., redirect_url: str = ...) -> Response:
        ...
    
    async def logout_user(self, request: Request) -> None:
        ...
    
    async def get_current_user(self, request: Request):
        ...
    
    def __call__(self, f: Callable[..., Any | Awaitable[Any]]) -> Callable[..., Any | Awaitable[Any]]:
        ...
    
    def fresh(self, f: Callable[..., Any | Awaitable[Any]]) -> Callable[..., Any | Awaitable[Any]]:
        ...
