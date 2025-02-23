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

from synthora.memories.base import BaseMemory
from synthora.messages.base import BaseMessage
from synthora.types.enums import MessageRole


class RecentNMemory(BaseMemory):
    def __init__(self, n: int) -> None:
        super().__init__()
        self.n = n

    def append(self, message: BaseMessage) -> None:
        super().append(message)
        if len(self) > self.n:
            self._remove_exceeded_messages()

    async def async_append(self, message: BaseMessage) -> None:
        self.append(message)

    def _remove_exceeded_messages(self) -> None:
        messages_to_remove = filter(
            lambda message: message.role != MessageRole.SYSTEM, self
        )

        while len(self) > self.n and messages_to_remove:
            self.remove(next(messages_to_remove))
