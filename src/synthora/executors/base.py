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

from abc import ABC
from typing import List, Union

from synthora.agents.base import BaseAgent
from synthora.models.base import BaseModelBackend
from synthora.toolkits.base import BaseFunction


ItemType = Union[BaseAgent, BaseFunction, BaseModelBackend]


class BaseExecutor(ABC):
    def __init__(self, can_be_root: bool) -> None:
        self.can_be_root = can_be_root

    def wrap(self, item: ItemType) -> ItemType:
        return item

    def wraps(self, items: List[ItemType]) -> List[ItemType]:
        return [self.wrap(item) for item in items]