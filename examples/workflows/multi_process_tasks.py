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

from synthora.workflows import BaseTask, ProcessPoolScheduler
from synthora.workflows.scheduler.base import BaseScheduler


def add(x: int, y: int) -> int:
    return x + y


flow = ProcessPoolScheduler()

(
    flow
    >> BaseTask(add)
    >> BaseTask(add).s(1)
    >> BaseTask(add).s(2)
    >> BaseTask(add).s(3)
)

print(flow.run(1, 2))

flow1 = ProcessPoolScheduler()

flow1 | BaseTask(add).s(1) | BaseTask(add).s(2) | BaseTask(add).s(3)
flow1.s(1)

print(flow1.run())

flow2 = BaseScheduler.chain(
    BaseTask(add), BaseTask(add).s(1), BaseTask(add).s(2), BaseTask(add).s(3)
)
print(flow2.run(1, 1))

flow3 = BaseScheduler.group(
    BaseTask(add),
    BaseTask(add),
    BaseTask(add),
)
print(flow3.run(1, 1))

flow4 = BaseScheduler.map(BaseTask(add).s(1), range(5))
print(flow4.run())

flow5 = BaseScheduler.starmap(BaseTask(add), [(1, 1), (1, 2), (1, 3)])
print(flow5.run())
