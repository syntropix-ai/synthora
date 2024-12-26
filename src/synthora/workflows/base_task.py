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

from abc import ABC
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Self, Union
from uuid import uuid4

from synthora.types.enums import TaskState


if TYPE_CHECKING:
    from synthora.workflows.scheduler.base import BaseScheduler


class BaseTask(ABC):
    def __init__(
        self,
        func: Callable[..., Any],
        name: Optional[str] = None,
        immutable: bool = False,
        flat_result: bool = False,
    ) -> None:
        self.func = func
        self.name = name or str(uuid4())
        self.immutable = immutable
        self.state = TaskState.PENDING
        self.meta_data: Dict[str, Any] = {}
        self.on_error: Optional[Callable[..., Any]] = None
        self._args: List[Any] = []
        self._kwargs: Dict[str, Any] = {}
        self._result: Optional[Any] = None
        self.flat_result = flat_result

    def result(self) -> Optional[Any]:
        return self._result
    
    def reset(self) -> Self:
        self.state = TaskState.PENDING
        self._result = None
        return self

    def signature(
        self,
        args: List[Any],
        kwargs: Dict[str, Any],
        immutable: bool = False,
        on_error: Optional[Callable[..., Any]] = None,
    ) -> Self:
        self._args += list(args)
        self._kwargs.update(kwargs)
        self.immutable = immutable
        self.on_error = on_error
        return self

    def s(self, *args: Any, **kwargs: Dict[str, Any]) -> Self:
        self._args += list(args)
        self._kwargs.update(kwargs)
        return self

    def si(self, *args: Any, **kwargs: Dict[str, Any]) -> Self:
        self._args += list(args)
        self._kwargs.update(kwargs)
        self.immutable = True
        return self

    def set_immutable(self, immutable: bool) -> Self:
        self.immutable = immutable
        return self

    def __call__(self, *args: Any, **kwargs: Dict[str, Any]) -> Any:
        if self.immutable:
            self._result = self.func(*self._args, **self._kwargs)
            return self._result
        args += tuple(self._args)
        kwargs.update(self._kwargs)
        self._result = self.func(*args, **kwargs)
        return self._result

    def __or__(self, other: Union["BaseScheduler", "BaseTask"]) -> "BaseScheduler":
        from synthora.utils.default import DEFAULT_GROUP_SCHEDULER

        return DEFAULT_GROUP_SCHEDULER() | self | other

    def __rshift__(self, other: Union["BaseScheduler", "BaseTask"]) -> "BaseScheduler":
        from synthora.utils.default import DEFAULT_CHAIN_SCHEDULER

        return DEFAULT_CHAIN_SCHEDULER() >> self >> other
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name


class AsyncTask(BaseTask):
    async def __call__(self, *args: Any, **kwargs: Dict[str, Any]) -> Any:
        if self.immutable:
            self._result = await self.func(*self._args, **self._kwargs)
            return self._result
        args += tuple(self._args)
        kwargs.update(self._kwargs)
        self._result = await self.func(*args, **kwargs)
        return self._result
