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

import json
import textwrap

from synthora.agents.vanilla_agent import VanillaAgent
from synthora.callbacks.rich_output_handler import RichOutputHandler
from synthora.configs import AgentConfig


json_data = textwrap.dedent(
    """\
    {
      "name": "Agent 1111",
      "type": "vanilla",
      "description": "Agent11",
      "model": {
        "model_type": "gpt-4o-mini",
        "name": "gpt-4",
        "backend": "openai_chat",
        "config": {
          "stream": true
        }
      },
      "prompt": "You are an AI Assistant. You are here to help me with my queries. Your name is vanilla.",
      "tools": [
        {
          "target": "synthora.agents.VanillaAgent",
          "trace": true,
          "args": {
            "name": "Agent 3",
            "type": "vanilla",
            "description": "Agent",
            "model": {
              "model_type": "gpt-4o-mini",
              "name": "gpt-4",
              "backend": "openai_chat",
              "config": {
                "stream": true
              }
            },
            "prompt": "You are an AI Assistant. You are here to help me with my queries. Your name is vanilla.",
            "tools": [
              {
                "target": "synthora.toolkits.search_toolkit.SearchToolkit",
                "trace": true,
                "args": {}
              }
            ]
          }
        },
        {
          "target": "synthora.toolkits.search_toolkit.SearchToolkit",
          "trace": true,
          "args": {}
        }
      ]
    }
    """  # noqa: E501
)

data = json.loads(json_data)
config = AgentConfig.from_dict(data)
agent = VanillaAgent.from_config(config)
agent.add_handler(RichOutputHandler())

agent.run("Search Openai on Wikipedia")
