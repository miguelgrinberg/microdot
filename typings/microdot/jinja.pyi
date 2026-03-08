from typing import Any, AsyncIterator, Awaitable, Iterator
from jinja2 import Environment, Template as JinjaTemplate

class Template:
    jinja_env: Environment
    @classmethod
    def initialize(cls, template_dir: str = ..., enable_async: bool = ..., **kwargs) -> None:
        ...
    
    name: str
    template: JinjaTemplate
    def __init__(self, template: str, **kwargs: Any) -> None:
        ...
    
    def generate(self, *args: Any, **kwargs: Any) -> Iterator[str]:
        ...
    
    def render(self, *args: Any, **kwargs: Any) -> str:
        ...
    
    def generate_async(self, *args: Any, **kwargs: Any) -> AsyncIterator[str]:
        ...
    
    async def render_async(self, *args: Any, **kwargs: Any) -> Awaitable[str]:
        ...
