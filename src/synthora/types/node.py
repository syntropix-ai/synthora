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

from typing import Optional

from pydantic import BaseModel

from synthora.types.enums import NodeType


class Node(BaseModel):
    """A model representing a node in the agent execution tree.

    This class captures detailed information about nodes in the agent execution
    tree, including their name, type, and ancestor.

    Attributes:
        name:
            The name of the node.
        type:
            The type of the node.
        ancestor:
            The ancestor of the node, defaults to None.
    """

    name: str
    type: NodeType
    ancestor: Optional["Node"] = None
