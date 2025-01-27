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

import datetime

import dotenv

from synthora.agents import VanillaAgent
from synthora.callbacks import RichOutputHandler
from synthora.prompts import BasePrompt
from synthora.toolkits.weather import WeatherToolkit
from synthora.triggers import TimeTrigger


dotenv.load_dotenv()

prompt = BasePrompt(
    """You are an AI assistant. Your name is Vanilla. Current time is:
    2025-01-27 01:21:15. If you call
    a tool at a specific time, the result will not return to you.
    If you need the result, please call yourself at that time.
    """
)

trigger = TimeTrigger(beat=1)
tool = WeatherToolkit().get_weather_data

trigger.add(tool)
trigger.start()

agent = VanillaAgent.default(
    prompt=prompt,
    tools=[tool],
    handlers=[RichOutputHandler()],
)
# print(agent.schema)

agent.add_tool(trigger.wrap_agent(agent))

for t in agent.tools:
    print(t.name)

while True:
    inp = input("Enter a search query: ")
    if inp == "exit":
        break
    time_str = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    res = agent.run(inp)

trigger.stop()
