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

from synthora.toolkits.decorators import tool


@tool
def add(a: int, b: int) -> int:
    r"""Add two numbers together."""
    return a + b


print(json.dumps(add.schema, indent=2))
print(add(1, 2))

# {
#     "type": "function",
#     "function": {
#         "name": "add",
#         "description": "Add two numbers together.",
#         "parameters": {
#             "properties": {
#                 "a": {"title": "A", "type": "integer"},
#                 "b": {"title": "B", "type": "integer"},
#             },
#             "required": ["a", "b"],
#             "title": "add",
#             "type": "object",
#         },
#     },
# }
# Ok(value=3)
