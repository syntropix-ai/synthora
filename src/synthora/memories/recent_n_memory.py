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

from synthora.memories.base import BaseMemory
from synthora.messages.base import BaseMessage
from synthora.types.enums import MessageRole


class RecentNMemory(BaseMemory):
    def __init__(self, n: int) -> None:
        super().__init__()
        self._n = n
        self._count = 0

    def append(self, message: BaseMessage) -> None:
        if message.role != MessageRole.SYSTEM:
            self._count += 1

        if self._count > self._n:
            self._remove_exceeded_messages()

        super().append(message)

    def _remove_exceeded_messages(self) -> None:
        messages_to_remove = []

        for message in self:
            if message.role == MessageRole.SYSTEM:
                continue
            messages_to_remove.append(message)
            self._count -= 1
            if self._count <= self._n:
                break

        for message in messages_to_remove:
            self.remove(message)
