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
from typing import Dict, List

from synthora.agents import VanillaAgent
from synthora.agents.base import BaseAgent
from synthora.configs import AgentConfig
from synthora.messages.base import BaseMessage
from synthora.workflows import task
from synthora.workflows.scheduler.thread_pool import ThreadPoolScheduler


warnings.filterwarnings("ignore")


@task
def generate_data(agent: BaseAgent, prompt: str) -> List[BaseMessage]:
    _ = agent.run(prompt)
    return agent.history


@task
def convert(*resps: List[BaseMessage]) -> List[Dict[str, str]]:
    data = []
    for resp in resps:
        data.append(
            {
                "prompt": str(resp[0].content),
                "instruct": str(resp[1].content),
                "response": str(resp[2].content),
            }
        )
    return data


config = AgentConfig.from_file("examples/workflows/configs/vanilla_agent.yaml")

prompts = [
    "What is the capital of France?",
    "What is the capital of Germany?",
]
agents = [VanillaAgent.from_config(config) for _ in range(len(prompts))]

flow = ThreadPoolScheduler.starmap(generate_data, zip(agents, prompts)) >> convert

data = flow.run()

for d in data:
    print(d)
    print("=" * 30)
