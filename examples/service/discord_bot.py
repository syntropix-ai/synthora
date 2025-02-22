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

import textwrap

from synthora.agents import VanillaAgent
from synthora.memories import RecentNMemory
from synthora.services.discord_bot import DiscordBotService
from synthora.toolkits.search_toolkits.google_search import search_google
from synthora.toolkits.webpage_toolkit import get_webpage


prompt = textwrap.dedent(
    """\
    You are a Discord Bot named OrcaNova. Your purpose is to respond to messages in a professional and engaging manner.
    The query you are given is a message from a user in the following format:

    <username> (<userid>) said: <message>

    Use markdown formatting for your responses, ensuring clarity and readability. When responding:

    Address users using <@userid> for mentions.
    Use markdown formatting for your responses, ensuring clarity and readability.
    Always aim for concise, helpful, and engaging communication.
    """  # noqa: E501
)

agent = VanillaAgent.default(prompt, tools=[get_webpage, search_google])
agent.history = RecentNMemory(100)

service = DiscordBotService()
service.add(agent).run()
