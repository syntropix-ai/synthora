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

from synthora.types.enums import TaskState
from synthora.workflows import BaseTask
from synthora.workflows.context.base import BaseContext
from synthora.workflows.scheduler.base import BaseScheduler


def add(ctx: BaseContext) -> int:
    with ctx:
        a = ctx.get('a', 1)
        b = ctx.get('b', 1)
        ctx['ans'] = a + b
        ctx['a'] = a + 1
        ctx['b'] = b + 1
        if a + b < 5:
            ctx.set_cursor(-1)
    return a + b


flow = BaseScheduler() >> BaseTask(add) >> BaseTask(add).si()


print(flow.run(), flow.get_context()["ans"])