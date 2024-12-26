from multiprocessing.managers import SyncManager
from threading import Lock
from typing import Any, Optional, Union, TYPE_CHECKING
from synthora.types.enums import TaskState
from synthora.workflows.base_task import BaseTask
from synthora.workflows.context.base import BaseContext
if TYPE_CHECKING:
    from synthora.workflows.scheduler.base import BaseScheduler


class ManagerContext(dict, BaseContext):
    def __init__(self, data: Any, lock: Lock, workflow: "BaseScheduler") -> None:
        super().__init__()
        self._data = data
        self._data["__workflow"] = workflow
        self._data["__lock"] = lock

    @property
    def lock(self) -> Lock:
        return self._data["__lock"]

    def acquire(self) -> None:
        self.lock.acquire()

    def release(self) -> None:
        self.lock.release()

    def get_task(self, name: str) -> Optional[Union["BaseScheduler", BaseTask]]:
        return self.workflow.get_task(name)

    def end(self) -> None:
        workflow = self.workflow
        workflow.state = TaskState.COMPLETED
        self._data["__workflow"] = workflow

    def skip(self, name: str) -> None:
        workflow = self.workflow
        if not (task := workflow.get_task(name)):
            raise KeyError(f"Task {name} not found")
        task.state = TaskState.SKIPPED
        self._data["__workflow"] = workflow

    def __getitem__(self, key: str) -> Any:
        if not key.startswith("__"):
            return self._data[key]
        raise KeyError(f"Key {key} is not allowed")

    def __setitem__(self, key: str, value: Any) -> None:
        if not key.startswith("__"):
            self._data[key] = value
        else:
            raise KeyError(f"Key {key} is not allowed")

    def get_state(self, name: str) -> TaskState:
        if task := self.get_task(name):
            return task.state
        raise KeyError(f"Task {name} not found")

    def set_state(self, name: str, state: TaskState) -> None:
        workflow = self.workflow
        if task := workflow.get_task(name):
            task.state = state
            self._data["__workflow"] = workflow
        else:
            raise KeyError(f"Task {name} not found")

    def get_result(self, name: str) -> Any:
        if task := self.get_task(name):
            return task.result()
        raise KeyError(f"Task {name} not found")

    def set_result(self, name: str, result: Any) -> None:
        workflow = self.workflow
        if task := workflow.get_task(name):
            task._result = result
            self._data["__workflow"] = workflow
        else:
            raise KeyError(f"Task {name} not found")

    @property
    def workflow(self) -> "BaseScheduler":
        return self._data["__workflow"]

    def __contains__(self, key):
        return self._data.__contains__(key)
