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

from dotenv import load_dotenv
from synthora.agents.vanilla_agent import VanillaAgent
from synthora.memories.summary_memory import SummaryMemory
from synthora.services.slack_bot import SlackBotService
from synthora.toolkits.search_toolkits.google_search import google_search
from synthora.toolkits.search_toolkits.webpage import webpage


load_dotenv()

prompt = """You are a Slack Bot named Synthora. Your purpose is to respond to messages in a professional and engaging manner.
Use Slack's mrkdwn formatting for your responses, ensuring clarity and readability. When responding:



Address users using <@user> for mentions.
Always use Slack's markdown formatting for output, for example:
    Use *text* for bold emphasis(not **text**), _text_ for italics, and inline code formatting using `code` where appropriate.
    Do not use # for headings, instead use * for bold text.
    NEVER use ** for bold text!!! Instead use * for bold text!!!
Provide structured lists and block quotes (>), where needed, to organize information.
Always aim for concise, helpful, and engaging communication.
NEVER use ** for bold text!!! Instead use * for bold text!!!
"""

agent = VanillaAgent.default(prompt, tools=[webpage, google_search])
agent.history = SummaryMemory(10, 5)

service = SlackBotService()

service.add(agent, "agent").run()
