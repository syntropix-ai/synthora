# LICENSE HEADER MANAGED BY add-license-header
#
# Copyright 2024-2025 Syntropix-AI.org
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

from synthora.agents.vanilla_agent import VanillaAgent
from synthora.prompts import BasePrompt


prompt = BasePrompt("Your name is {username}")

# print(prompt.format(username="John Doe"))

agent = VanillaAgent.default(prompt)

print(agent.run("what is your name?", username="John Doe"))