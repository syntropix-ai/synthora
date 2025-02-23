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

import inspect
from typing import Any, Callable, Optional

from .base_task import AsyncTask, BaseTask
from .context import BasicContext, MultiProcessContext
from .scheduler import BaseScheduler, ProcessPoolScheduler, ThreadPoolScheduler


def task(
    func: Optional[Callable[..., Any]] = None,
    *,
    name: Optional[str] = None,
    immutable: bool = False,
) -> BaseTask:
    if func is None:

        def decorator(inner_func: Callable[..., Any]) -> BaseTask:
            if inspect.iscoroutinefunction(inner_func):
                return AsyncTask(
                    inner_func,
                    name=name,
                    immutable=immutable,
                )
            return BaseTask(
                inner_func,
                name=name,
                immutable=immutable,
            )

        return decorator  # type: ignore[return-value]
    else:
        if inspect.iscoroutinefunction(func):
            return AsyncTask(
                func,
                name=name,
                immutable=immutable,
            )
        return BaseTask(
            func,
            name=name,
            immutable=immutable,
        )


__all__ = [
    "BaseTask",
    "AsyncTask",
    "BaseScheduler",
    "ProcessPoolScheduler",
    "ThreadPoolScheduler",
    "task",
    "BasicContext",
    "MultiProcessContext",
]
