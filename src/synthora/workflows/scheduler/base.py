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

from abc import ABC

from synthora.workflows.base_task import AsyncTask, BaseTask


class BaseScheduler(ABC):
    def __init__(self, flat_result: bool = False):
        self.flat_result = flat_result
        self.states = {}
        self.tasks = []
        self.cursor = 0
        self._result = None

    def result(self):
        return self._result

    def add_task(self, task):
        self.tasks.append([task])

    def add_tasks(self, *tasks):
        for task in tasks:
            self.add_task(task)

    def add_task_group(self, group):
        self.tasks.append(list(group))

    def __or__(self, value):
        if isinstance(value, BaseTask) or isinstance(value, BaseScheduler):
            if not self.tasks:
                self.add_task(value)
            else:
                self.tasks[-1].append(value)
            return self
        else:
            raise ValueError("Invalid value, must be a Task or Scheduler")

    def __rshift__(self, value):
        if isinstance(value, BaseTask) or isinstance(value, BaseScheduler):
            self.add_task(value)
            return self
        else:
            raise ValueError("Invalid value, must be a Task or Scheduler")

    def _get_result(self, tasks):
        if tasks is None:
            return []
        result = []
        for task in tasks:
            if task.flat_result:
                result.extend(task.result())
            else:
                result.append(task.result())
        return result

    def _run(self, pre, current, *args, **kwargs):
        prev_args = self._get_result(pre)
        args = prev_args + list(args)
        if isinstance(current, BaseTask):
            current(*args, **kwargs)
        elif isinstance(current, BaseScheduler):
            current.run(*args, **kwargs)

    async def _async_run(self, pre, current, *args, **kwargs):
        prev_args = self._get_result(pre)
        args = prev_args + list(args)
        if isinstance(current, AsyncTask):
            await current(*args, **kwargs)
        elif isinstance(current, BaseTask):
            current(*args, **kwargs)
        elif isinstance(current, BaseScheduler):
            current.async_run(*args, **kwargs)

    def step(self, *args, **kwargs):
        if self.cursor >= len(self.tasks):
            return None
        pre = self.tasks[self.cursor - 1] if self.cursor > 0 else None
        current = self.tasks[self.cursor]
        for task in current:
            self._run(pre, task, *args, **kwargs)
        self.cursor += 1

    def run(self, *args, **kwargs):
        if len(self.tasks) == 0:
            raise RuntimeError("No tasks to run")
        self.step(*args, **kwargs)
        while self.cursor < len(self.tasks):
            self.step()
        self._result = self._get_result(self.tasks[-1])
        if len(self._result) == 1:
            self._result = self._result[0]
        return self._result

    async def async_step(self, *args, **kwargs):
        if self.cursor >= len(self.tasks):
            return None
        pre = self.tasks[self.cursor - 1] if self.cursor > 0 else None
        current = self.tasks[self.cursor]
        for task in current:
            await self._async_run(pre, task, *args, **kwargs)
        self.cursor += 1

    async def async_run(self, *args, **kwargs):
        if len(self.tasks) == 0:
            raise RuntimeError("No tasks to run")
        await self.async_step(*args, **kwargs)
        while self.cursor < len(self.tasks):
            await self.async_step()
        self._result = self._get_result(self.tasks[-1])
        if len(self._result) == 1:
            self._result = self._result[0]
        return self._result
