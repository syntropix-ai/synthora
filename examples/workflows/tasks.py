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

from synthora.workflows import BaseScheduler, BaseTask


def add(x: int, y: int) -> int:
    return x + y


flow = BaseScheduler()

(
    flow
    >> BaseTask(add)
    >> BaseTask(add).s(1)
    >> BaseTask(add).s(2)
    >> BaseTask(add).s(3)
)

print(flow.run(1, 2))

flow = BaseScheduler()

flow | BaseTask(add).s(1) | BaseTask(add).s(2) | BaseTask(add).s(3)

print(flow.run(1))

flow = BaseScheduler()

flow | BaseTask(add).s(1) | BaseTask(add).s(2) | BaseTask(add).si(1, 2)

print(flow.run(1))

flow1 = BaseScheduler(flat_result=True)
flow2 = BaseScheduler()

flow1 | BaseTask(add).si(1, 1) | BaseTask(add).si(1, 2)
flow2 >> BaseTask(add).s(1) >> flow1 >> BaseTask(add) | BaseTask(add).si(1, 2)
print(flow2.run(1))
