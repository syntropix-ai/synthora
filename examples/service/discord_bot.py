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

import textwrap
from typing import List, Union

from synthora.agents import BaseAgent, VanillaAgent
from synthora.memories import RecentNMemory
from synthora.services.discord_bot import DiscordBotService
from synthora.toolkits import BaseFunction, SearchToolkit, WeatherToolkit
from synthora.toolkits.search_toolkits import MediawikiToolkit


prompt = textwrap.dedent(
    """\
    You are a Discord Bot in a Server. Each user in the server has a username and unique user ID. Your name is OrcaNova and your ID is 1325529446370906293.
    Your purpose is to respond to messages in a professional and engaging manner.
    The query you are given is a message from a user in the following format:

    <username> (<userid>) said: <message>

    Note that, in the message content, each mention will be presented as <@userid>.

    Use markdown formatting for your responses, ensuring clarity and readability. When responding:

    Address users using <@userid> for mentions.
    Use markdown formatting for your responses, ensuring clarity and readability.
    Always aim for concise, helpful, and engaging communication.

    There are something important to know:
    - There will be messages from different users in the history
    - Use the history to understand the context of the conversation, PAY EXTRA ATTENTION TO THE USER THAT SENT EACH MESSAGE, DON'T MIX THEM UP
    """  # noqa: E501
)

tools: List[Union[BaseFunction, BaseAgent]] = [
    SearchToolkit().search_all,
    WeatherToolkit().get_weather_data,
    *MediawikiToolkit("https://moegirl.uk/api.php").sync_tools,
]
agent = VanillaAgent.default(prompt, tools=tools)
agent.history = RecentNMemory(50)

service = DiscordBotService()
service.add(agent).run()
