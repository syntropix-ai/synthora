# LICENSE HEADER MANAGED BY add-license-header
#
# Copyright 2024-2025 Syntropix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from asyncio import Task
from typing import TYPE_CHECKING, Any, Literal, Optional, Union


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from synthora.agents.base import BaseAgent
from synthora.models.base import BaseModelBackend
from synthora.services.base import BaseService
from synthora.toolkits.base import BaseFunction
from synthora.types import HttpAgentRequest
from synthora.workflows.base_task import BaseTask
from synthora.workflows.scheduler.base import BaseScheduler


if TYPE_CHECKING:
    from fastapi import FastAPI
    from uvicorn import Server


def _add_agent_to_app(
    app: "FastAPI",
    agent: BaseAgent,
    name: Optional[str] = None,
    method: Literal["get", "post"] = "post",
    use_async: bool = True,
) -> None:
    decorator = app.get if method == "get" else app.post
    if use_async:

        async def endpoint(request: HttpAgentRequest) -> Any:
            return await agent.async_run(
                request.message,
                *(request.args or []),
                **(request.kwargs or {}),
            )

    else:

        def endpoint(request: HttpAgentRequest) -> Any:
            return agent.run(
                request.message,
                *(request.args or []),
                **(request.kwargs or {}),
            )

    decorator(f"/{name}", response_model=None)(endpoint)


class HttpService(BaseService):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__()
        try:
            import uvicorn  # noqa
            from fastapi import FastAPI
        except ImportError:
            raise ImportError("FastAPI or uvicorn is not installed")
        self.app = FastAPI(*args, **kwargs)
        self.server: Optional[Server] = None
        self.server_task: Optional[Task[Any]] = None

    def add(
        self,
        target: Union[
            BaseFunction, BaseAgent, BaseModelBackend, BaseTask, BaseScheduler
        ],
        name: Optional[str] = None,
        method: Literal["get", "post"] = "post",
        use_async: bool = True,
    ) -> Self:
        if isinstance(target, BaseAgent):
            name = name or target.name
            self.service_map[name] = target
            _add_agent_to_app(self.app, target, name, method, use_async)
        else:
            raise NotImplementedError(
                f"Unsupported target type: {type(target)}"
            )
        return self

    async def async_run(
        self, host: str = "127.0.0.1", port: int = 8000
    ) -> None:
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

    def stop(self) -> Self:
        import asyncio

        asyncio.run(self.async_stop())
        return self
