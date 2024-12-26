from multiprocessing.managers import SyncManager
from threading import Lock
from typing import Any, Optional, Union, TYPE_CHECKING
from synthora.types.enums import TaskState
from synthora.workflows.base_task import BaseTask
from synthora.workflows.context.base import BaseContext
if TYPE_CHECKING:
    from synthora.workflows.scheduler.base import BaseScheduler


class ManagerContext(SyncManager, BaseContext):
    def __init__(self, workflow: "BaseScheduler") -> None:
        super().__init__()
        self.start()

        self.data = self.dict()
        self.data["__workflow"] = workflow
        self.data["__lock"] = self.Lock()

    @property
    def lock(self) -> Lock:
        return self.data["__lock"]

    def acquire(self) -> None:
        self.lock.acquire()

    def release(self) -> None:
        self.lock.release()

    def get_task(self, name: str) -> Optional[Union["BaseScheduler", BaseTask]]:
        return self.workflow.get_task(name)

    def end(self) -> None:
        self.workflow.state = TaskState.COMPLETED

    def skip(self, name: str) -> None:
        self.get_task(name).state = TaskState.SKIPPED

    def __getitem__(self, key: str) -> Any:
        if not key.startswith("__"):
            return self.data[key]
        raise KeyError(f"Key {key} is not allowed")

    def __setitem__(self, key: str, value: Any) -> None:
        if not key.startswith("__"):
            self.data[key] = value
        else:
            raise KeyError(f"Key {key} is not allowed")

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
        return self.data["__workflow"]
