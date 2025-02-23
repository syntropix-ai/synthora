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


from synthora.agents import VanillaAgent
from synthora.configs import AgentConfig
from synthora.memories.recent_n_memory import RecentNMemory


config = AgentConfig.from_file("examples/agents/configs/vanilla_agent.yaml")
# print(config)

agent = VanillaAgent.from_config(config)
agent.history = RecentNMemory(3)

while True:
    user_input = input("Enter a query: ")
    if user_input == "exit":
        break
    print(agent.run(user_input).unwrap().content)

    print("History:")
    for message in agent.history:
        print(f"{message.role}: {message.content}")
