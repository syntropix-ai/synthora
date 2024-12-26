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

from typing import TYPE_CHECKING, Any, Optional, Union

from synthora.types.enums import TaskState
from synthora.workflows.base_task import BaseTask
from synthora.workflows.context.base import BaseContext


if TYPE_CHECKING:
    from synthora.workflows.scheduler.base import BaseScheduler


class BasicContext(dict, BaseContext):
    def __init__(self, workflow: "BaseScheduler") -> None:
        super().__init__()
        self._workflow = workflow

    @property
    def lock(self) -> None:
        pass

    def acquire(self) -> None:
        pass

    def release(self) -> None:
        pass

    def get_task(self, name: str) -> Optional[Union["BaseScheduler", BaseTask]]:
        return self._workflow.get_task(name)

    def end(self) -> None:
        self._workflow.state = TaskState.COMPLETED

    def skip(self, name: str) -> None:
        self.get_task(name).state = TaskState.SKIPPED

    def get_state(self, name: str) -> TaskState:
        if task := self.get_task(name):
            return task.state
        raise KeyError(f"Task {name} not found")

    def set_state(self, name: str, state: TaskState) -> None:
        if task := self.get_task(name):
            task.state = state
        else:
            raise KeyError(f"Task {name} not found")

    def get_result(self, name: str) -> Any:
        if task := self.get_task(name):
            return task.result()
        raise KeyError(f"Task {name} not found")

    def set_result(self, name: str, result: Any) -> None:
        if task := self.get_task(name):
            task._result = result
        else:
            raise KeyError(f"Task {name} not found")

    @property
    def workflow(self) -> "BaseScheduler":
        return self._workflow
