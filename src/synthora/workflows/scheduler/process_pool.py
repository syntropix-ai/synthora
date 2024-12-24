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

from concurrent.futures import ProcessPoolExecutor
from typing import Optional

from synthora.workflows.base_task import BaseTask
from synthora.workflows.scheduler.base import BaseScheduler


class ProcessPoolScheduler(BaseScheduler):
    def __init__(self, max_worker: Optional[int] = None, flat_result: bool = False):
        self.max_worker = max_worker
        super().__init__(flat_result)

    def _run(self, executor, pre, current, *args, **kwargs):
        prev_args = self._get_result(pre)
        args = prev_args + list(args)
        if isinstance(current, BaseTask):
            return executor.submit(current, *args, **kwargs)
        elif isinstance(current, BaseScheduler):
            return executor.submit(current.run, *args, **kwargs)

    async def _async_run(self, pre, current, *args, **kwargs):
        raise NotImplementedError("ProcessPoolScheduler does not support async tasks")

    def step(self, *args, **kwargs):
        if self.cursor >= len(self.tasks):
            return None
        pre = self.tasks[self.cursor - 1] if self.cursor > 0 else None
        current = self.tasks[self.cursor]
        with ProcessPoolExecutor(self.max_worker) as pool:
            futures = [self._run(pool, pre, task, *args, **kwargs) for task in current]
            for task, future in zip(current, futures):
                task._result = future.result()
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
        raise NotImplementedError("ProcessPoolScheduler does not support async tasks")

    async def async_run(self, *args, **kwargs):
        raise NotImplementedError("ProcessPoolScheduler does not support async tasks")
