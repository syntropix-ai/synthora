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

import textwrap

from synthora.memories.base import BaseMemory
from synthora.messages import system, user
from synthora.messages.base import BaseMessage
from synthora.models import BaseModelBackend
from synthora.types.enums import MessageRole


class SummaryMemory(BaseMemory):
    def __init__(self, n: int, summary_model: BaseModelBackend) -> None:
        super().__init__()
        self._n = n
        self._count = 0
        self._summary_model = summary_model

    def append(self, message: BaseMessage) -> None:
        if message.role != MessageRole.SYSTEM:
            self._count += 1

        if self._count > self._n:
            self._summarize()

        super().append(message)

    def _summarize(self) -> None:
        messages_to_summarize = []
        cache = []

        for message in self:
            if message.role == MessageRole.SYSTEM:
                continue
            cache.append(message)
            if message.role == MessageRole.USER:
                messages_to_summarize += cache
                cache = []

        history_str = "Here is the history of the conversation:\n<history>\n"
        last_user_message = messages_to_summarize[-1]
        for message in messages_to_summarize[:-1]:
            self.remove(message)
            history_str += f"{message.role.value}: {message.content}\n"
        history_str += "</history>\nNow make an objective summary of the conversation in third person. Only return the summary, no other text."

        history = [system("You are a helpful assistant."), user(history_str)]

        summary = self._summary_model.run(history).content
        last_user_message.content = textwrap.dedent(
            f"""\
            This is the summary of our previous conversation:
            <summary>
            {summary}
            </summary>
            Now the query is:
            {last_user_message.content}
            """
        )
