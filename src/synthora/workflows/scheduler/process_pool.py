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

from concurrent.futures import Future, ProcessPoolExecutor, as_completed
from multiprocessing.managers import SyncManager
from typing import Any, List, Optional, Union

from synthora.types.enums import TaskState
from synthora.workflows.base_task import BaseTask
from synthora.workflows.context.multiprocess_context import MultiProcessContext
from synthora.workflows.scheduler.base import BaseScheduler


class ProcessPoolScheduler(BaseScheduler):
    def __init__(
        self,
        name: Optional[str] = None,
        context: Optional[MultiProcessContext] = None,
        max_worker: Optional[int] = None,
        flat_result: bool = False,
        immutable: bool = False,
    ) -> None:
        self.max_worker = max_worker
        super().__init__(name, context, flat_result, immutable)

    def _run(  # type: ignore[override]
        self,
        executor: ProcessPoolExecutor,
        pre: Optional[List[Union["BaseScheduler", BaseTask]]],
        current: Union["BaseScheduler", BaseTask],
        *args: Any,
        **kwargs: Any,
    ) -> Future[Any]:
        prev_args = self._get_result(pre)
        args = tuple(prev_args) + args
        if isinstance(current, BaseTask):
            if self.need_context(current):
                return executor.submit(current, self.context, *args, **kwargs)
            return executor.submit(current, *args, **kwargs)
        elif isinstance(current, BaseScheduler):
            return executor.submit(current.run, *args, **kwargs)

    async def _async_run(
        self,
        pre: Optional[List[Union["BaseScheduler", BaseTask]]],
        current: Union["BaseScheduler", BaseTask],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        raise NotImplementedError(
            "ProcessPoolScheduler does not support async tasks"
        )

    def step(self, *args: Any, **kwargs: Any) -> None:
        if self.cursor >= len(self.tasks):
            return None
        pre = self.tasks[self.cursor - 1] if self.cursor > 0 else None
        current = self.tasks[self.cursor]
        self.get_context().set_cursor(self.cursor)
        with ProcessPoolExecutor(self.max_worker) as pool:
            futures = []
            for task in current:
                if (
                    self.get_context().get_state(task.name)
                    != TaskState.SKIPPED
                ):
                    self.get_context().set_state(task.name, TaskState.RUNNING)
                    task.state = TaskState.RUNNING
                    futures.append(self._run(pool, pre, task, *args, **kwargs))

            as_completed(futures)
            for task, future in zip(current, futures):
                try:
                    task._result = future.result()
                    task.state = TaskState.COMPLETED
                    self.get_context().set_result(task.name, task._result)
                    self.get_context().set_state(
                        task.name, TaskState.COMPLETED
                    )
                except Exception:
                    self.get_context().set_state(task.name, TaskState.FAILURE)
                    task.meta_data["error"] = future.exception()
                    self.state = TaskState.FAILURE
                    self.get_context().set_state(self.name, TaskState.FAILURE)

        self.cursor = self.get_context().get_cursor() + 1

    def run(self, *args: Any, **kwargs: Any) -> Any:
        if len(self.tasks) == 0:
            raise RuntimeError("No tasks to run")
        if self.context is None:
            manager = SyncManager()
            manager.start()
            data = manager.dict()
            lock = manager.Lock()
            context = MultiProcessContext(data, lock, self)
            self.set_context(context)
        cursor = self.get_context().get_cursor()
        self.state = TaskState.RUNNING
        self.get_context().set_state(self.name, TaskState.RUNNING)
        if self.immutable:
            self.step(*self._args, **self._kwargs)
        else:
            args = tuple(self._args) + args
            kwargs = {**self._kwargs, **kwargs}
            self.step(*args, **kwargs)
        while self.cursor < len(self.tasks):
            state = self.get_context().get_state(self.name)
            if state != TaskState.RUNNING:
                break
            self.step()
        self._result = self._get_result(self.tasks[self.cursor - 1])
        if len(self._result) == 1:
            self._result = self._result[0]
        self.get_context().set_result(self.name, self._result)
        if self.cursor == len(self.tasks):
            self.get_context().set_state(self.name, TaskState.COMPLETED)
            self.state = TaskState.COMPLETED
        self.get_context().set_cursor(cursor)
        return self._result

    async def async_step(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError(
            "ProcessPoolScheduler does not support async tasks"
        )

    async def async_run(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError(
            "ProcessPoolScheduler does not support async tasks"
        )
