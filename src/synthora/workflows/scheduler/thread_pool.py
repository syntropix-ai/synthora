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

from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Dict, List, Optional, Union, override

from synthora.types.enums import TaskState
from synthora.workflows.base_task import BaseTask
from synthora.workflows.context.basic_context import BasicContext
from synthora.workflows.scheduler.base import BaseScheduler


class ThreadPoolScheduler(BaseScheduler):
    def __init__(
        self,
        name: Optional[str] = None,
        context: Optional[BasicContext] = None,
        max_worker: Optional[int] = None,
        flat_result: bool = False,
        immutable: bool = False,
    ):
        self.max_worker = max_worker
        super().__init__(name, context, flat_result, immutable)

    @override
    def _run(  # type: ignore[override]
        self,
        executor: ThreadPoolExecutor,
        pre: Optional[List[Union["BaseScheduler", BaseTask]]],
        current: Union["BaseScheduler", BaseTask],
        *args: Any,
        **kwargs: Dict[str, Any],
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
        **kwargs: Dict[str, Any],
    ) -> None:
        raise NotImplementedError("ThreadPoolScheduler does not support async tasks")

    def step(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        if self.cursor >= len(self.tasks):
            return None
        pre = self.tasks[self.cursor - 1] if self.cursor > 0 else None
        current = self.tasks[self.cursor]
        self.get_context().set_cursor(self.cursor)
        with ThreadPoolExecutor(self.max_worker) as pool:
            futures = []
            for task in current:
                if task.state != TaskState.SKIPPED:
                    task.state = TaskState.RUNNING
                    futures.append(self._run(pool, pre, task, *args, **kwargs))

            for task, future in zip(current, futures):
                try:
                    task._result = future.result()
                    task.state = TaskState.COMPLETED
                except Exception:
                    task.state = TaskState.FAILURE
                    task.meta_data["error"] = future.exception()

        self.cursor = self.get_context().get_cursor() + 1

    def run(self, *args: Any, **kwargs: Dict[str, Any]) -> Any:
        if len(self.tasks) == 0:
            raise RuntimeError("No tasks to run")
        if self.context is None:
            self.set_context(BasicContext(self))

        self.state = TaskState.RUNNING
        if self.immutable:
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
        self.state = TaskState.COMPLETED
        return self._result

    async def async_step(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        raise NotImplementedError("ThreadPoolScheduler does not support async tasks")

    async def async_run(self, *args: Any, **kwargs: Dict[str, Any]) -> Any:
        raise NotImplementedError("ThreadPoolScheduler does not support async tasks")
