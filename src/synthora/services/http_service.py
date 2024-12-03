from typing import Any, Callable, Dict, Literal, Optional, Self, Union

from synthora.agents.base import BaseAgent
from synthora.models.base import BaseModelBackend
from synthora.services.base import BaseService
from synthora.toolkits.base import BaseFunction
import inspect

def _add_agent_to_app(app, agent: BaseAgent, name: Optional[str] = None, method: Literal["get", "post"] = "post", use_async: bool = True) -> None:
    decorator = app.get if method == "get" else app.post
    
    target_method = agent.async_run if use_async else agent.run
    sig = inspect.signature(target_method)
    params = list(sig.parameters.values())
    if params and params[0].name == 'self':
        params = params[1:]
    params = [p for p in params if p.kind != p.VAR_POSITIONAL]
    
    sig = sig.replace(parameters=params)
    bound_method = target_method.__get__(agent)
    if use_async:
        async def endpoint(**kwargs):
            return await bound_method(**kwargs)
    else:
        def endpoint(**kwargs):
            return bound_method(**kwargs)

    endpoint.__signature__ = sig
    endpoint.__annotations__ = target_method.__annotations__

    decorator(f"/{name}", response_model=None)(endpoint)

class HttpService(BaseService):
    def __init__(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        super().__init__()
        try:
            from fastapi import FastAPI
            import uvicorn
        except ImportError:
            raise ImportError("FastAPI or uvicorn is not installed")
        self.app = FastAPI(*args, **kwargs)
        
    
    def add(self, target: Union[BaseFunction, BaseAgent, BaseModelBackend], name: Optional[str] = None, method: Literal["get", "post"] = "post", use_async: bool = True) -> Self:
        if isinstance(target, BaseAgent):
            name = name or target.name
            self.service_map[name] = target
            _add_agent_to_app(self.app, target, name, method, use_async)
        else:
            raise NotImplementedError(f"Unsupported target type: {type(target)}")
        
    async def async_run(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        import asyncio
        from uvicorn import Config, Server
        config = Config(app=self.app, host=host, port=port, loop="asyncio")
        self.server = Server(config)
        self.server_task = asyncio.create_task(self.server.serve())
    
    async def async_stop(self) -> None:
        if self.server and self.server_task:
            self.server.should_exit = True
            await self.server_task
            
    def run(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)
        
    def stop(self) -> None:
        import asyncio
        asyncio.run(self.async_stop())
        
    
