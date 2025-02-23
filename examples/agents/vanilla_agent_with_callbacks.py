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


import json
import warnings

from synthora.agents import VanillaAgent
from synthora.callbacks import RichOutputHandler
from synthora.configs import AgentConfig


warnings.filterwarnings("ignore")

config = AgentConfig.from_file("examples/agents/configs/basic_agent.yaml")

print(json.dumps(config.model_dump(), indent=2))
# exit(0)
agent = VanillaAgent.from_config(config)
# print(agent.callback_manager, agent.tools[-1].callback_manager)
# print(agent.schema)
handler = RichOutputHandler()
agent.add_handler(handler)


# print(agent.callback_manager.handlers)
# print(agent.tools[-1].callback_manager.handlers)

# agent.run("What's your name?")
# agent.run("119 * 117 = ?")
agent.run("Search Openai on Wikipedia")
