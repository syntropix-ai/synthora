# LICENSE HEADER MANAGED BY add-license-header
#
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
#

import inspect
from typing import TYPE_CHECKING, Any, Dict, Literal, Optional, Self, Union

from synthora.agents.base import BaseAgent
from synthora.models.base import BaseModelBackend
from synthora.services.base import BaseService
from synthora.toolkits.base import BaseFunction


if TYPE_CHECKING:
    from uvicorn import Server


def _add_agent_to_app(
    app,
    agent: BaseAgent,
    name: Optional[str] = None,
    method: Literal["get", "post"] = "post",
    use_async: bool = True,
) -> None:
    decorator = app.get if method == "get" else app.post

    target_method = agent.async_run if use_async else agent.run
    sig = inspect.signature(target_method)
    params = list(sig.parameters.values())
    if params and params[0].name == "self":
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
            import uvicorn
            from fastapi import FastAPI
        except ImportError:
            raise ImportError("FastAPI or uvicorn is not installed")
        self.app = FastAPI(*args, **kwargs)
        self.server: Optional[Server] = None
        self.server_task = None

    def add(
        self,
        target: Union[BaseFunction, BaseAgent, BaseModelBackend],
        name: Optional[str] = None,
        method: Literal["get", "post"] = "post",
        use_async: bool = True,
    ) -> Self:
        if isinstance(target, BaseAgent):
            name = name or target.name
            self.service_map[name] = target
            _add_agent_to_app(self.app, target, name, method, use_async)
        else:
            raise NotImplementedError(f"Unsupported target type: {type(target)}")
        return self

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

    def run(self, host: str = "127.0.0.1", port: int = 8000) -> Self:
        import uvicorn

        uvicorn.run(self.app, host=host, port=port)
        return self

    def stop(self) -> None:
        import asyncio

        asyncio.run(self.async_stop())
