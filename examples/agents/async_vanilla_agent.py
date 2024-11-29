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
from synthora.callbacks.rich_output_handler import RichOutputHandler
from synthora.configs import AgentConfig
import asyncio


config = AgentConfig.from_file("examples/agents/configs/vanilla_agent.yaml")

agent = VanillaAgent.from_config(config)
print(json.dumps(agent.schema, indent=2))
agent.add_handler(RichOutputHandler())


asyncio.run(agent.async_run("Search Openai on Wikipedia"))
