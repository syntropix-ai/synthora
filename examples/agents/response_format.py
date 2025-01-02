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


from synthora.agents import VanillaAgent
from synthora.configs import AgentConfig
from synthora.utils import get_pydantic_model


config = AgentConfig.from_file(
    "examples/agents/configs/vanilla_agent_without_tools.yaml"
)

resp_format = get_pydantic_model(
    '{"location": "Beijing", "date": "2023-09-01", "temperature": 30.0}'
)

agent = VanillaAgent.from_config(config)
agent.model.config["response_format"] = get_pydantic_model(resp_format)
del agent.model.config["stream"]

print(
    agent.run("Format: Today is 2023-09-01, the temperature in Beijing is 30 degrees.")
)