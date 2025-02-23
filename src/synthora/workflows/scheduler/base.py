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
from copy import deepcopy
from inspect import signature
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Union,
    get_type_hints,
)
from uuid import uuid4


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from synthora.types.enums import TaskState
from synthora.workflows.base_task import AsyncTask, BaseTask
from synthora.workflows.context.base import BaseContext
from synthora.workflows.context.basic_context import BasicContext


class BaseScheduler(ABC):
    def __init__(
        self,
        name: Optional[str] = None,
        context: Optional[BaseContext] = None,
        flat_result: bool = False,
        immutable: bool = False,
    ) -> None:
        self.name = name or str(uuid4())
        self.context = context
        self.flat_result = flat_result
        self.tasks: List[List[Union[BaseScheduler, BaseTask]]] = []
        self.cursor = 0
        self._result: Optional[Any] = None
        self.immutable = immutable
        self._args: List[Any] = []
        self._kwargs: Dict[str, Any] = {}
        self.state = TaskState.PENDING
        self.meta_data: Dict[str, Any] = {}

    def get_task(
        self, name: str
    ) -> Optional[Union["BaseScheduler", BaseTask]]:
        if self.name == name:
            return self
        for task_group in self.tasks:
            for task in task_group:
                if task.name == name:
                    return task
                if isinstance(task, BaseScheduler):
                    sub_task = task.get_task(name)
                    if sub_task:
                        return sub_task
        return None

    def get_workflow_by_task(self, name: str) -> Optional["BaseScheduler"]:
        for task_group in self.tasks:
            for task in task_group:
                if task.name == name:
                    return self
                if isinstance(task, BaseScheduler):
                    sub_task = task.get_workflow_by_task(name)
                    if sub_task:
                        return sub_task
        return None

    def signature(
        self,
        *args: Any,
        immutable: bool = False,
        **kwargs: Any,
    ) -> Self:
        self._args = list(args)
        self._kwargs = kwargs
        self.immutable = immutable
        return self

    def s(self, *args: Any, **kwargs: Any) -> Self:
        self._args = list(args)
        self._kwargs = kwargs
        return self

    def si(self, *args: Any, **kwargs: Any) -> Self:
        self._args = list(args)
        self._kwargs = kwargs
        self.immutable = True
        return self

    def set_immutable(self, immutable: bool) -> Self:
        self.immutable = immutable
        return self

    def set_flat_result(self, flat_result: bool) -> Self:
        self.flat_result = flat_result
        return self

    @classmethod
    def chain(
        cls,
        *tasks: Union[
            List[Union["BaseScheduler", BaseTask]],
            Union["BaseScheduler", BaseTask],
        ],
        **kwargs: Any,
    ) -> Self:
        return cls(**kwargs).add_tasks(*tasks)  # type: ignore[arg-type]

    @classmethod
    def group(
        cls,
        *tasks: Union[
            List[Union["BaseScheduler", BaseTask]],
            Union["BaseScheduler", BaseTask],
        ],
        **kwargs: Any,
    ) -> Self:
        return cls(**kwargs).add_task_group(tasks)  # type: ignore[arg-type]

    @classmethod
    def map(
        cls,
        workflow: Union["BaseScheduler", BaseTask],
        data: Iterable[Any],
        config: Dict[str, Any] = {},
    ) -> Self:
        scheduler = cls(**config)
        tasks = [deepcopy(workflow).s(item) for item in data]
        for task in tasks:
            task.name = str(uuid4())
        return scheduler.add_task_group(tasks)

    @classmethod
    def starmap(
        cls,
        workflow: Union["BaseScheduler", BaseTask],
        data: Iterable[Any],
        config: Dict[str, Any] = {},
    ) -> Self:
        scheduler = cls(**config)
        tasks = []
        for item in data:
            tasks.append(
                deepcopy(workflow).s(**item)
                if isinstance(item, dict)
                else deepcopy(workflow).s(*item)
            )
            tasks[-1].name = str(uuid4())
        return scheduler.add_task_group(tasks)

    def result(self) -> Optional[Any]:
        return self._result

    def add_task(self, task: Union["BaseScheduler", BaseTask]) -> Self:
        if not isinstance(task, BaseTask) and not isinstance(
            task, BaseScheduler
        ):
            raise ValueError("Invalid value, must be a Task or Scheduler")
        self.tasks.append([task])
        return self

    def add_tasks(self, *tasks: Union["BaseScheduler", BaseTask]) -> Self:
        for task in tasks:
            self.add_task(task)
        return self

    def add_task_group(
        self, group: List[Union["BaseScheduler", BaseTask]]
    ) -> Self:
        for task in group:
            if not isinstance(task, BaseTask) and not isinstance(
                task, BaseScheduler
            ):
                raise ValueError("Invalid value, must be a Task or Scheduler")
        self.tasks.append(list(group))
        return self

    def __or__(
        self, value: Union["BaseScheduler", BaseTask]
    ) -> "BaseScheduler":
        if isinstance(value, BaseTask):
            new_scheduler = deepcopy(self) if self.tasks else self
            if not new_scheduler.tasks:
                new_scheduler.add_task(value)
            else:
                new_scheduler.tasks[-1].append(value)
            return new_scheduler
        else:
            raise ValueError("Invalid value, must be a Task")

    def __invert__(self) -> Self:
        self.tasks.append([])
        return self

    def __rshift__(
        self, value: Union["BaseScheduler", BaseTask]
    ) -> "BaseScheduler":
        if isinstance(value, BaseTask) or isinstance(value, BaseScheduler):
            new_scheduler = self.__class__() if self.tasks else self
            if new_scheduler is self:
                new_scheduler.add_task(value)
            else:
                new_scheduler.add_task(self)
                new_scheduler.add_task(value)
                new_scheduler.flat_result = value.flat_result
                new_scheduler.immutable = value.immutable

            return new_scheduler
        else:
            raise ValueError("Invalid value, must be a Task or Scheduler")

    def _get_result(
        self, tasks: Optional[List[Union["BaseScheduler", BaseTask]]]
    ) -> List[Any]:
        if tasks is None:
            return []
        result: List[Any] = []
        for task in tasks:
            if task.flat_result:
                result.extend(task.result())  # type: ignore[arg-type]
            else:
                result.append(task.result())
        return result

    def _run(
        self,
        pre: Optional[List[Union["BaseScheduler", BaseTask]]],
        current: Union["BaseScheduler", BaseTask],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        prev_args = self._get_result(pre)
        _args = prev_args + list(args)
        if isinstance(current, BaseTask):
            if self.need_context(current):
                current(self.context, *_args, **kwargs)
            else:
                current(*_args, **kwargs)
        elif isinstance(current, BaseScheduler):
            current.run(*_args, **kwargs)

    async def _async_run(
        self,
        pre: Optional[List[Union["BaseScheduler", BaseTask]]],
        current: Union["BaseScheduler", BaseTask],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        prev_args = self._get_result(pre)
        args = tuple(prev_args) + args
        if isinstance(current, AsyncTask):
            if self.need_context(current):
                await current(self.context, *args, **kwargs)
            else:
                await current(*args, **kwargs)
        elif isinstance(current, BaseTask):
            if self.need_context(current):
                current(self.context, *args, **kwargs)
            else:
                current(*args, **kwargs)
        elif isinstance(current, BaseScheduler):
            await current.async_run(*args, **kwargs)

    def step(self, *args: Any, **kwargs: Any) -> None:
        if self.cursor >= len(self.tasks):
            return None
        pre = self.tasks[self.cursor - 1] if self.cursor > 0 else None
        current = self.tasks[self.cursor]
        self.get_context().set_cursor(self.name, self.cursor)
        for task in current:
            if task.state != TaskState.SKIPPED:
                task.state = TaskState.RUNNING
                try:
                    self._run(pre, task, *args, **kwargs)
                    task.state = TaskState.COMPLETED
                except Exception as e:
                    task.state = TaskState.FAILURE
                    task.meta_data["error"] = str(e)

        self.cursor = self.get_context().get_cursor(self.name) + 1

    def run(self, *args: Any, **kwargs: Any) -> Any:
        if len(self.tasks) == 0:
            raise RuntimeError("No tasks to run")
        if self.context is None:
            self.set_context(BasicContext(self))
        cursor = self.get_context().get_cursor(self.name)
        self.state = TaskState.RUNNING
        if self.immutable:
            if args and isinstance(args[0], BaseContext):
                self.step(args[0], *self._args, **self._kwargs)
            else:
                self.step(*self._args, **self._kwargs)
        else:
            args = tuple(self._args) + args
            kwargs = {**self._kwargs, **kwargs}
            self.step(*args, **kwargs)
        while self.cursor < len(self.tasks):
            if self.state != TaskState.RUNNING:
                break
            self.step()
        self._result = self._get_result(self.tasks[self.cursor - 1])
        if len(self._result) == 1:
            self._result = self._result[0]
        self.get_context().set_result(self.name, self._result)
        self.get_context().set_cursor(self.name, cursor)
        return self._result

    async def async_step(self, *args: Any, **kwargs: Any) -> None:
        if self.cursor >= len(self.tasks):
            return None
        pre = self.tasks[self.cursor - 1] if self.cursor > 0 else None
        current = self.tasks[self.cursor]
        self.get_context().set_cursor(self.name, self.cursor)
        for task in current:
            if task.state != TaskState.SKIPPED:
                task.state = TaskState.RUNNING
                try:
                    await self._async_run(pre, task, *args, **kwargs)
                    task.state = TaskState.COMPLETED
                except Exception as e:
                    task.state = TaskState.FAILURE
                    task.meta_data["error"] = str(e)
        self.cursor = self.get_context().get_cursor(self.name) + 1

    async def async_run(self, *args: Any, **kwargs: Any) -> Any:
        if len(self.tasks) == 0:
            raise RuntimeError("No tasks to run")
        if self.context is None:
            self.set_context(BasicContext(self))
        cursor = self.get_context().get_cursor(self.name)
        self.state = TaskState.RUNNING
        if self.immutable:
            if args and isinstance(args[0], BaseContext):
                await self.async_step(args[0], *self._args, **self._kwargs)
            else:
                await self.async_step(*self._args, **self._kwargs)
        else:
            args = tuple(self._args) + args
            kwargs = {**self._kwargs, **kwargs}
            await self.async_step(*args, **kwargs)
        while self.cursor < len(self.tasks):
            if self.state != TaskState.RUNNING:
                break
            await self.async_step()
        self._result = self._get_result(self.tasks[self.cursor - 1])
        if len(self._result) == 1:
            self._result = self._result[0]
        self.get_context().set_result(self.name, self._result)
        self.get_context().set_cursor(self.name, cursor)
        return self._result

    def set_context(self, context: BaseContext) -> Self:
        self.context = context
        for task in self.tasks:
            for sub_task in task:
                if isinstance(sub_task, BaseScheduler):
                    sub_task.set_context(context)
        return self

    def need_context(self, task: BaseTask) -> bool:
        sig = signature(task.func)
        type_hints = get_type_hints(task.func)

        for name in sig.parameters:
            try:
                if name in type_hints and issubclass(
                    type_hints[name], BaseContext
                ):
                    return True
            except Exception:
                pass
        return False

    def reset(self) -> Self:
        self.cursor = 0
        self._result = None
        self.state = TaskState.PENDING
        for task_group in self.tasks:
            for task in task_group:
                task.reset()
        self.context = None
        return self

    def __str__(self) -> str:
        rep = f"{self.name}:\n"
        for task_group in self.tasks:
            for task in task_group:
                for i in str(task).split("\n"):
                    if i:
                        rep += f"\t{i}\n"
            rep += "\n"
        return rep

    def __repr__(self) -> str:
        return self.__str__()

    def get_context(self) -> BaseContext:
        if self.context is None:
            raise ValueError("Context is not set")
        return self.context
