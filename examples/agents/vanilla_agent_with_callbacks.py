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

import json

from synthora.agents import VanillaAgent
from synthora.configs import AgentConfig
from synthora.callbacks import BaseCallBackHandler, RichOutputHandler

import warnings
warnings.filterwarnings("ignore")

config = AgentConfig.from_file("examples/agents/configs/vanilla_agent.yaml")

# class MyHandler(BaseCallBackHandler):
#     def on_tool_start(self, source, *args, **kwargs):
#         print("Tool Start")
#         print(source)
#         print(args)
#         print(kwargs)

#     def on_tool_end(self, source, result):
#         print("Tool End")
#         print(source)
#         print(result)

#     def on_tool_error(self, source, result):
#         print("Tool Error")
#         print(source)
#         print(result)
# print(config)

agent = VanillaAgent.from_config(config)
handler = RichOutputHandler()
agent.tools[0].callback_manager.add(handler)
agent.model.callback_manager.add(handler)
agent.callback_manager.add(handler)
# print(agent.tools[0].callback_manager)
# print(json.dumps(agent.schema, indent=2))
agent.run("Search Trump on Wikipedia")
# print(agent.run("Search Trump on Wikipedia"))

# for i in agent.history:
#     print(i)
# print(json.dumps(i, indent=2))
