from abc import ABC, abstractmethod
from typing import Any

from synthora.types.enums import TaskState


class BaseContext(ABC):

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
    def __getitem__(self, key: str) -> Any: ...

    @abstractmethod
    def __setitem__(self, key: str, value: Any) -> None: ...

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
