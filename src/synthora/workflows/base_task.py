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

from abc import ABC
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Union,
)


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self
from uuid import uuid4

from synthora.types.enums import TaskState


if TYPE_CHECKING:
    from synthora.workflows.scheduler.base import BaseScheduler


class BaseTask(ABC):
    """An abstract base class designed to serve as the foundation for tasks in
    the Synthora framework.

    Tasks are essential components of workflows, providing encapsulated and
    reusable logic.

    Attributes:
        func:
            The callable function that represents the core logic of the task.
        name:
            An optional name for the task. If not provided, a UUID is
            automatically assigned.
        immutable:
            Indicates whether the task is immutable, preventing modifications
            to its arguments or state.
        flat_result:
            Not used.
        state:
            The current state of the task, initialized as `TaskState.PENDING`.
        meta_data:
            A dictionary to store task-specific metadata.
        _args:
            A list to hold positional arguments for the task.
        _kwargs:
            A dictionary to hold keyword arguments for the task.
        _result:
            The computed result of the task. Initialized to `None`.
    """

    def __init__(
        self,
        func: Callable[..., Any],
        name: Optional[str] = None,
        immutable: bool = False,
        flat_result: bool = False,
    ) -> None:
        """Initialize the BaseTask.

        Args:
            func:
                The callable function that represents the core logic of the
                task.
            name:
                An optional name for the task. If not provided, a UUID is
                automatically assigned.
            immutable:
                Indicates whether the task is immutable, preventing
                modifications to its arguments or state.
            flat_result:
                Not used.
        """
        self.func = func
        self.name = name or str(uuid4())
        self.immutable = immutable
        self.state = TaskState.PENDING
        self.meta_data: Dict[str, Any] = {}
        self._args: List[Any] = []
        self._kwargs: Dict[str, Any] = {}
        self._result: Optional[Any] = None
        self.flat_result = flat_result

    def result(self) -> Optional[Any]:
        """Return the computed result of the task.

        Returns:
            The computed result of the task.
        """
        return self._result

    def reset(self, clear_arguments: bool = False) -> Self:
        """Reset the task to its initial state.

        Args:
            clear_arguments:
                Indicates whether to clear the arguments of the task.
        Returns:
            The task instance in its initial state.
        """
        self.state = TaskState.PENDING
        self._result = None
        if clear_arguments:
            self._args = []
            self._kwargs = {}
        return self

    def signature(
        self,
        *args: List[Any],
        immutable: bool = False,
        **kwargs: Dict[str, Any],
    ) -> Self:
        """Set the signature of the task.

        Signature is a method to set the arguments and keyword arguments of the
        task. By doing so, the task can be executed with the provided arguments
        and keyword arguments when called, without the need to pass them again.

        Args:
            args:
                A list of positional arguments.
            kwargs:
                A dictionary of keyword arguments.
            immutable:
                Indicates whether the task is immutable.

        Returns:
            The task instance with the provided signature.
        """
        self._args = list(args)
        self._kwargs = kwargs
        self.immutable = immutable
        return self

    def s(self, *args: Any, **kwargs: Any) -> Self:
        """Set the signature of the task.

        This is a shorthand method to set the arguments and keyword arguments
        of the task.

        Args:
            *args:
                A list of positional arguments.
            **kwargs:
                A dictionary of keyword arguments.

        Returns:
            The task instance with the provided signature.
        """
        self._args = list(args)
        self._kwargs = kwargs
        return self

    def si(self, *args: Any, **kwargs: Any) -> Self:
        """Set the signature of the task and make it immutable.

        This is a shorthand method to set the arguments and keyword arguments
        of the task.

        Args:
            *args:
                A list of positional arguments.
            **kwargs:
                A dictionary of keyword arguments.

        Returns:
            The task instance with the provided signature.
        """
        self._args = list(args)
        self._kwargs = kwargs
        self.immutable = True
        return self

    def set_immutable(self, immutable: bool) -> Self:
        """Set the task as immutable.

        Args:
            immutable:
                Indicates whether the task is immutable.

        Returns:
            The task instance with the provided immutability status.
        """
        self.immutable = immutable
        return self

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Call the task.

        Args:
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            The computed result of the task.
        """
        if self.immutable:
            from synthora.workflows.context.base import BaseContext

            if args and isinstance(args[0], BaseContext):
                self._result = self.func(args[0], *self._args, **self._kwargs)
            else:
                self._result = self.func(*self._args, **self._kwargs)
            return self._result
        args += tuple(self._args)
        kwargs.update(self._kwargs)
        self._result = self.func(*args, **kwargs)
        return self._result

    def __or__(
        self, other: Union["BaseScheduler", "BaseTask"]
    ) -> "BaseScheduler":
        """Compose the task with another task or scheduler using the OR
        operator.

        Args:
            other:
                Another task or scheduler.

        Returns:
            A new scheduler instance that composes the tasks.
        """
        from synthora.utils.default import DEFAULT_GROUP_SCHEDULER

        return DEFAULT_GROUP_SCHEDULER() | self | other

    def __rshift__(
        self, other: Union["BaseScheduler", "BaseTask"]
    ) -> "BaseScheduler":
        r"""Compose the task with another task or scheduler using the RIGHT
        SHIFT operator.

        Args:
            other:
                Another task or scheduler.

        Returns:
            A new scheduler instance that composes the tasks.
        """
        from synthora.utils.default import DEFAULT_CHAIN_SCHEDULER

        flow = DEFAULT_CHAIN_SCHEDULER() >> self >> other

        flow.flat_result = other.flat_result
        return flow

    def __str__(self) -> str:
        r"""Return the string representation of the task.

        Returns:
            The string representation of the task.
        """
        return self.name

    def __repr__(self) -> str:
        r"""Return the string representation of the task.

        Returns:
            The string representation of the task.
        """
        return self.name

    def run(self, *args: Any, **kwargs: Any) -> Any:
        r"""Call the task.

        Args:
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            The computed result of the task.
        """
        return self(*args, **kwargs)

    async def async_run(self, *args: Any, **kwargs: Any) -> Any:
        r"""Call the task asynchronously.

        Args:
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            The computed result of the task.
        """
        raise NotImplementedError


class AsyncTask(BaseTask):
    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Call the task asynchronously.

        Args:
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            The computed result of the task.
        """
        if self.immutable:
            from synthora.workflows.context.base import BaseContext

            if args and isinstance(args[0], BaseContext):
                self._result = await self.func(
                    args[0], *self._args, **self._kwargs
                )
            else:
                self._result = await self.func(*self._args, **self._kwargs)
            return self._result
        args += tuple(self._args)
        kwargs.update(self._kwargs)
        self._result = await self.func(*args, **kwargs)
        return self._result

    async def async_run(self, *args: Any, **kwargs: Any) -> Any:
        r"""Call the task asynchronously.

        Args:
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            The computed result of the task.
        """
        return await self(*args, **kwargs)
