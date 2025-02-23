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

from synthora.workflows import BaseTask
from synthora.workflows.context.base import BaseContext
from synthora.workflows.scheduler.process_pool import ProcessPoolScheduler


def add(ctx: BaseContext, x: int, y: int) -> int:
    with ctx:
        print(ctx.get_state(f"{x + y}"))
        if "ans" not in ctx:
            ctx["ans"] = [x + y]
        else:
            ctx["ans"] = ctx["ans"] + [x + y]
    return x + y


flow = ProcessPoolScheduler()
(
    flow
    | BaseTask(add, "2").s(1)
    | BaseTask(add, "3").s(2)
    | BaseTask(add, "4").s(3)
)


print(flow.run(1), flow.get_context()["ans"])
