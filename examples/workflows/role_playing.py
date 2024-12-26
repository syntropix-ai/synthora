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


import warnings

from synthora.agents import VanillaAgent
from synthora.configs import AgentConfig
from synthora.types.enums import Result
from synthora.workflows import BaseTask
from synthora.workflows.scheduler.thread_pool import ThreadPoolScheduler


warnings.filterwarnings("ignore")

config = AgentConfig.from_file("examples/workflows/configs/vanilla_agent.yaml")

agent1 = VanillaAgent.from_config(config)
agent2 = VanillaAgent.from_config(config)


def convert(resp: Result[str, Exception]) -> str:
    return resp.unwrap()


prompt1 = "Please debate: What came first, the chicken or the egg? Your argument is that the egg came first."
prompt2 = "Please debate: What came first, the chicken or the egg? Your argument is that the chicken came first."

for round in range(2):
    flow1 = (BaseTask(agent1.run) >> BaseTask(convert)).s(prompt1)
    flow2 = (BaseTask(agent2.run) >> BaseTask(convert)).s(prompt2)
    flow = ThreadPoolScheduler.group(flow1, flow2)

    prompt2, prompt1 = flow.run()
    print(prompt1)
    print("=" * 30)
    print(prompt2)