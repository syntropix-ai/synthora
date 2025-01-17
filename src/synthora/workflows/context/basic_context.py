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

from typing import TYPE_CHECKING, Any, Optional, Union

from synthora.types.enums import TaskState
from synthora.workflows.base_task import BaseTask
from synthora.workflows.context.base import BaseContext


if TYPE_CHECKING:
    from synthora.workflows.scheduler.base import BaseScheduler


class BasicContext(BaseContext):


    """
    BasicContext class provides a context for managing the state and results of tasks within a workflow.

    Attributes:
        _workflow (BaseScheduler): The workflow associated with this context.
        _cursor (int): The current cursor position within the workflow.

    Methods:
        lock: Property that represents a lock mechanism (not implemented).
        acquire: Acquire the lock (not implemented).
        release: Release the lock (not implemented).
        get_task(name: str) -> Optional[Union[BaseScheduler, BaseTask]]: Retrieve a task by its name.
        end: Mark the workflow as completed.
        skip(name: str) -> None: Skip a task by its name.
        get_state(name: str) -> TaskState: Get the state of a task by its name.
        set_state(name: str, state: TaskState) -> None: Set the state of a task by its name.
        get_result(name: str) -> Any: Get the result of a task by its name.
        set_result(name: str, result: Any) -> None: Set the result of a task by its name.
        workflow: Property that returns the associated workflow.
        get_cursor() -> int: Get the current cursor position.
        set_cursor(cursor: int) -> None: Set the cursor position.
        __contains__(key: Any) -> bool: Check if a key is in the context.
        __getitem__(key: Any) -> Any: Get an item by key.
        __setitem__(key: Any, value: Any) -> None: Set an item by key.
    """
    def __init__(self, workflow: "BaseScheduler") -> None:
        """
        Initialize the BasicContext.

        Args:
            workflow (BaseScheduler): The workflow instance to be used by the context.
        """
        super().__init__()
        self._workflow = workflow
        self._cursor = 0

    @property
    def lock(self) -> None:
        pass

    def acquire(self) -> None:
        pass

    def release(self) -> None:
        pass

    def get_task(
        self, name: str
    ) -> Optional[Union["BaseScheduler", BaseTask]]:
        return self._workflow.get_task(name)

    def end(self) -> None:
        self._workflow.state = TaskState.COMPLETED

    def skip(self, name: str) -> None:
        if task := self.get_task(name):
            task.state = TaskState.SKIPPED

    def get_state(self, name: str) -> TaskState:
        """
        Retrieve the state of a task by its name.

        Args:
            name (str): The name of the task.

        Returns:
            TaskState: The state of the task.

        Raises:
            KeyError: If the task with the given name is not found.
        """
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

    def get_cursor(self) -> int:
        return self._cursor

    def set_cursor(self, cursor: int) -> None:
        self._cursor = cursor

    def __contains__(self, key: Any) -> bool:
        return super().__contains__(key)

    def __getitem__(self, key: Any) -> Any:
        return super().__getitem__(key)

    def __setitem__(self, key: Any, value: Any) -> None:
        return super().__setitem__(key, value)
