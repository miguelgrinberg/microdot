from typing import Any, AsyncIterator, Awaitable, Callable, Iterator

class Template:
    name: str
    template: Callable[..., Iterator[str]]
    @classmethod
    def initialize(cls, template_dir: str = ..., loader_class: type | None = ...) -> None:
        ...
    
    def __init__(self, template: str) -> None:
        ...
    
    def generate(self, *args: Any, **kwargs: Any) -> Iterator[str]:
        ...
    
    def render(self, *args: Any, **kwargs: Any) -> str:
        ...
    
    def generate_async(self, *args: Any, **kwargs: Any) -> AsyncIterator[str]:
        ...
    
    async def render_async(self, *args: Any, **kwargs: Any) -> Awaitable[str]:
        ...
