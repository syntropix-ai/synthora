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

import asyncio
import json

from synthora.toolkits.basic_math_toolkit import BasicMathToolkit


loop = asyncio.new_event_loop()

toolkit = BasicMathToolkit()
print([i.name for i in toolkit.sync_tools])
print(toolkit.async_add.name, loop.run_until_complete(toolkit.async_add(1, 2)))  # type: ignore[arg-type]

print(toolkit.add.name, toolkit.add(1, 2))
print(toolkit.subtract.name, toolkit.subtract(1, 2))
print(toolkit.multiply.name, toolkit.multiply(1, 2))
print(toolkit.divide.name, toolkit.divide(1, 2))
print(toolkit.divide.name, toolkit.divide(1, 0))

print(json.dumps(toolkit.async_add.schema, indent=2))


# ['add', 'subtract', 'multiply', 'divide']
# async_add Ok(value=3)
# add Ok(value=3)
# subtract Ok(value=-1)
# multiply Ok(value=2)
# divide Ok(value=0.5)
# divide Err(error=ZeroDivisionError('Cannot divide by zero'))
# {
#   "type": "function",
#   "function": {
#     "name": "async_add",
#     "description": "Add two numbers together",
#     "parameters": {
#       "properties": {
#         "a": {
#           "anyOf": [
#             {
#               "type": "integer"
#             },
#             {
#               "type": "number"
#             }
#           ],
#           "title": "A",
#           "description": "The first number"
#         },
#         "b": {
#           "anyOf": [
#             {
#               "type": "integer"
#             },
#             {
#               "type": "number"
#             }
#           ],
#           "title": "B",
#           "description": "The second number"
#         }
#       },
#       "required": [
#         "a",
#         "b"
#       ],
#       "title": "async_add",
#       "type": "object"
#     }
#   }
# }
