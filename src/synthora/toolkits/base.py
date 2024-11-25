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
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========

import asyncio
import inspect
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Union, cast

from synthora.callbacks.base_handler import BaseCallBackHandler
from synthora.callbacks.base_manager import AsyncCallBackManager, BaseCallBackManager
from synthora.types import Err, Ok, Result
from synthora.types.enums import CallBackEvent, NodeType
from synthora.types.node import Node
from synthora.utils import get_openai_tool_schema


class BaseFunction(ABC):
    def __init__(
        self,
        instance: Any,
        func: Callable[..., Any],
        source: Optional[Node] = None,
        callback_manager: BaseCallBackManager = BaseCallBackManager(),
    ) -> None:
        self.instance = instance
        self.func = func
        self.schema = get_openai_tool_schema(func)
        self.source: Node = source or Node(name=self.name, type=NodeType.TOOL)
        self.callback_manager = callback_manager

    @staticmethod
    def wrap(
        func: Callable[..., Any],
        instance: Optional[Any] = None,
        source: Optional[Node] = None,
        handlers: List[BaseCallBackHandler] = [],
    ) -> Union["SyncFunction", "AsyncFunction"]:
        if isinstance(func, staticmethod):
            instance = None

        if asyncio.iscoroutinefunction(func) or asyncio.iscoroutinefunction(
            inspect.unwrap(func)
        ):
            callback_manager = AsyncCallBackManager(handlers=handlers)
            return AsyncFunction(instance, func, source, callback_manager)
        else:
            callback_manager = BaseCallBackManager(handlers=handlers)
            return SyncFunction(instance, func, source, callback_manager)

    @property
    def name(self) -> str:
        return cast(str, self.schema["function"]["name"])

    @property
    def description(self) -> str:
        return cast(str, self.schema["function"]["description"])

    @property
    def parameters(self) -> Dict[str, Any]:
        return self.schema["function"]["parameters"]["properties"]  # type: ignore[no-any-return]

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Result[Any, Exception]: ...

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Result[Any, Exception]: ...

    @abstractmethod
    def async_run(self, *args: Any, **kwargs: Any) -> Result[Any, Exception]: ...

    def add_handler(
        self, handler: BaseCallBackHandler, recursive: bool = False
    ) -> None:
        self.callback_manager.add(handler)


class SyncFunction(BaseFunction):
    def __call__(self, *args: Any, **kwargs: Any) -> Result[Any, Exception]:
        try:
            if self.instance is not None:
                args = (self.instance,) + args
            resp = self.func(*args, **kwargs)
            if isinstance(resp, Result):
                return resp
            return Ok(resp)
        except Exception as e:
            return Err(e, str(e))

    def run(self, *args: Any, **kwargs: Any) -> Result[Any, Exception]:
        self.callback_manager.call(
            CallBackEvent.TOOL_START, self.source, *args, **kwargs
        )
        result = self(*args, **kwargs)
        if result.is_err:
            self.callback_manager.call(CallBackEvent.TOOL_ERROR, self.source, result)
        else:
            self.callback_manager.call(CallBackEvent.TOOL_END, self.source, result)
        return result

    def async_run(self, *args: Any, **kwargs: Any) -> Result[Any, Exception]:
        raise NotImplementedError("This function is not async")


class AsyncFunction(BaseFunction):
    async def __call__(self, *args: Any, **kwargs: Any) -> Result[Any, Exception]:  # type: ignore[override]
        try:
            if self.instance is not None:
                args = (self.instance,) + args
            resp = await self.func(*args, **kwargs)
            if isinstance(resp, Result):
                return resp
            return Ok(resp)
        except Exception as e:
            return Err(e, str(e))

    async def async_run(self, *args: Any, **kwargs: Any) -> Result[Any, Exception]:
        self.callback_manager.call(
            CallBackEvent.TOOL_START, self.source, *args, **kwargs
        )
        result = await self(*args, **kwargs)
        if result.is_err:
            await self.callback_manager.call(
                CallBackEvent.TOOL_ERROR, self.source, result
            )
        else:
            await self.callback_manager.call(
                CallBackEvent.TOOL_END, self.source, result
            )
        return result

    def run(self, *args: Any, **kwargs: Any) -> Result[Any, Exception]:
        raise NotImplementedError("This function is not sync")


class BaseToolkit(ABC):
    def __init__(self) -> None:
        self._exposed_functions = []

        for v in self.__class__.__dict__.values():
            if isinstance(v, BaseFunction):
                if getattr(v, "_flag", False):
                    v.instance = self
                self._exposed_functions.append(v)

    @property
    def sync_tools(self) -> List[BaseFunction]:
        return [f for f in self._exposed_functions if isinstance(f, SyncFunction)]

    @property
    def async_tools(self) -> List[BaseFunction]:
        return [f for f in self._exposed_functions if isinstance(f, AsyncFunction)]
