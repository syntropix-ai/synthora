# LICENSE HEADER MANAGED BY add-license-header
#
# Copyright 2024-2025 Syntropix-AI.org
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
from typing import Any, Optional

from synthora.workflows import task
from synthora.workflows.base_task import BaseTask

from .condition import if_else
from .loop import for_loop, while_loop


def empty(name: Optional[str] = None) -> BaseTask:
    @task(flat_result=True)
    def _empty(*args: Any, **kwargs: Any) -> Any:
        if kwargs:
            return *args, kwargs
        return args

    if name:
        _empty.name = name
    return _empty  # type: ignore[no-any-return]


__all__ = ["for_loop", "while_loop", "if_else", "empty"]
