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

from synthora.toolkits.search_toolkit import SearchToolkit


toolkit = SearchToolkit()

print([i.name for i in toolkit.sync_tools])

print(
    toolkit.search_wikipedia.name,
    toolkit.search_wikipedia("Python programming language"),
)

print(json.dumps(toolkit.search_wikipedia.schema, indent=2))

"""
['search_wikipedia']
search_wikipedia Ok(value='Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation.\nPython is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming. It is often described as a "batteries included" language due to its comprehensive standard library.')
{
  "type": "function",
  "function": {
    "name": "search_wikipedia",
    "description": "",
    "parameters": {
      "properties": {
        "query": {
          "title": "Query",
          "type": "string"
        },
        "sentences": {
          "default": 5,
          "title": "Sentences",
          "type": "integer"
        },
        "auto_suggest": {
          "default": false,
          "title": "Auto Suggest",
          "type": "boolean"
        }
      },
      "required": [
        "query"
      ],
      "title": "search_wikipedia",
      "type": "object"
    }
  }
}
"""  # noqa: E501
