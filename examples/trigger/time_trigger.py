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

import dotenv

from synthora.agents import VanillaAgent
from synthora.callbacks import RichOutputHandler
from synthora.toolkits.weather import WeatherToolkit
from synthora.triggers import TimeTrigger
from synthora.prompts import BasePrompt
import datetime

dotenv.load_dotenv()

prompt = BasePrompt(
    "You are an AI assistant. Current time is: {time}"
)

trigger = TimeTrigger()
tool = WeatherToolkit().get_weather_data

trigger.add(tool)
trigger.start()

agent = VanillaAgent.default(
    prompt=prompt,
    tools=[tool],  # type: ignore[arg-type]
    handlers=[RichOutputHandler()],
)

while True:
    inp = input("Enter a search query: ")
    if inp == "exit":
        break
    time_str = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    res = agent.run(inp, time=time_str)

trigger.stop()
