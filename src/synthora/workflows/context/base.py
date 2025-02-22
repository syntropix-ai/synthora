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

from abc import ABC, abstractmethod
from typing import Any, Dict

from synthora.types.enums import TaskState


class BaseContext(Dict[Any, Any], ABC):
    @property
    @abstractmethod
    def lock(self) -> Any: ...

    @abstractmethod
    def acquire(self) -> None: ...

    @abstractmethod
    def release(self) -> None: ...

    @abstractmethod
    def end(self) -> None: ...

    @abstractmethod
    def skip(self, name: str) -> None: ...

    @abstractmethod
    def __getitem__(self, key: str) -> Any:
        return super().__getitem__(key)

    @abstractmethod
    def __setitem__(self, key: str, value: Any) -> None:
        super().__setitem__(key, value)

    @abstractmethod
    def get_state(self, name: str) -> TaskState: ...

    @abstractmethod
    def set_state(self, name: str, state: TaskState) -> None: ...

    @abstractmethod
    def get_result(self, name: str) -> Any: ...

    @abstractmethod
    def set_result(self, name: str, result: Any) -> None: ...

    @abstractmethod
    def get_task(self, name: str) -> Any: ...

    @property
    @abstractmethod
    def workflow(self) -> Any: ...

    def __enter__(self) -> None:
        self.acquire()

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.release()

    @abstractmethod
    def get_cursor(self, id: str) -> int: ...

    @abstractmethod
    def set_cursor(self, id: str, cursor: int) -> None: ...
