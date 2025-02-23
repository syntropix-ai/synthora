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
from synthora.types.enums import MessageRole, NodeType
from synthora.types.node import Node

from .base import BaseMessage


def user(content: str) -> BaseMessage:
    return BaseMessage(
        role=MessageRole.USER,
        source=Node(name="user", type=NodeType.USER),
        content=content,
    )


def system(content: str) -> BaseMessage:
    return BaseMessage(
        role=MessageRole.SYSTEM,
        source=Node(name="system", type=NodeType.SYSTEM),
        content=content,
    )


def assistant(content: str, name: str = "assitant") -> BaseMessage:
    return BaseMessage(
        role=MessageRole.ASSISTANT,
        source=Node(name=name, type=NodeType.AGENT),
        content=content,
    )


__all__ = ["BaseMessage", "user", "system", "assistant"]
