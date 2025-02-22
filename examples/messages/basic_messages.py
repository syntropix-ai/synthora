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

from synthora.messages import BaseMessage
from synthora.types.enums import MessageRole, NodeType
from synthora.types.node import Node


user_message = BaseMessage.create_message(
    role=MessageRole.USER,
    content="Hello, Synthora!",
    source=Node(name="user", type=NodeType.USER),
    metadata={"user_id": "1234"},
)

user_message_with_image = BaseMessage.create_message(
    role=MessageRole.USER,
    content="Hello, Synthora!",
    images=["https://example.com/image.jpg"],
    source=Node(name="user", type=NodeType.USER),
    metadata={"user_id": "1234"},
)

function_response_message = BaseMessage.create_message(
    id="1234",
    role=MessageRole.TOOL_RESPONSE,
    content="Hello, Synthora!",
    source=Node(name="function", type=NodeType.TOOL),
    metadata={"tool_call_id": "1234"},
)


assistant_message = BaseMessage.create_message(
    role=MessageRole.ASSISTANT,
    content="Hello, Synthora!",
    source=Node(name="assistant", type=NodeType.AGENT),
    metadata={"assistant_id": "1234"},
)


print(user_message.to_openai_message())
print(user_message_with_image.to_openai_message())
print(function_response_message.to_openai_message())
print(assistant_message.to_openai_message())
