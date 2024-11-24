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
from abc import ABC
from typing import Any, Callable, Dict, List, Optional, Union, cast

from synthora.types import Err, Ok, Result
from synthora.utils import get_openai_tool_schema


class BaseFunction(ABC):
    def __init__(self, instance: Any, func: Callable[..., Any]) -> None:
        self.instance = instance
        self.func = func
        self.schema = get_openai_tool_schema(func)

    @staticmethod
    def wrap(
        func: Callable[..., Any],
        instance: Optional[Any] = None,
    ) -> Union["SyncFunction", "AsyncFunction"]:
        if isinstance(func, staticmethod):
            instance = None

        if asyncio.iscoroutinefunction(func) or asyncio.iscoroutinefunction(
            inspect.unwrap(func)
        ):
            return AsyncFunction(instance, func)
        else:
            return SyncFunction(instance, func)

    @property
    def name(self) -> str:
        return cast(str, self.schema["function"]["name"])

    @property
    def description(self) -> str:
        return cast(str, self.schema["function"]["description"])

    @property
    def parameters(self) -> Dict[str, Any]:
        return self.schema["function"]["parameters"]["properties"]  # type: ignore[no-any-return]


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


class AsyncFunction(BaseFunction):
    async def __call__(self, *args: Any, **kwargs: Any) -> Result[Any, Exception]:
        try:
            if self.instance is not None:
                args = (self.instance,) + args
            resp = await self.func(*args, **kwargs)
            if isinstance(resp, Result):
                return resp
            return Ok(resp)
        except Exception as e:
            return Err(e, str(e))


class BaseToolkit(ABC):
    def __init__(self) -> None:
        self._exposed_functions = [
            BaseFunction.wrap(v, self)
            for v in self.__class__.__dict__.values()
            if getattr(v, "_flag", False)
        ]
        for f in self._exposed_functions:
            setattr(self, f.name, f)
        for v in self.__class__.__dict__.values():
            if (
                issubclass(v.__class__, BaseFunction)
                and v not in self._exposed_functions
            ):
                self._exposed_functions.append(v)

    @property
    def sync_tools(self) -> List[BaseFunction]:
        return [f for f in self._exposed_functions if isinstance(f, SyncFunction)]

    @property
    def async_tools(self) -> List[BaseFunction]:
        return [f for f in self._exposed_functions if isinstance(f, AsyncFunction)]
