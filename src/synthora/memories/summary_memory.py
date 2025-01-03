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
    def __init__(
        self, n: int, cache_size: int, prompt: str, summary_model: BaseModelBackend
    ) -> None:
        super().__init__()
        self.n = n
        self.prompt = prompt
        self.cache_size = cache_size
        self.summary_model = summary_model

    def append(self, message: BaseMessage) -> None:
        super().append(message)
        if len(self) > self.n:
            self._summarize()

    def _summarize(self) -> None:
        messages_to_summarize = list(
            filter(lambda message: message.role != MessageRole.SYSTEM, self)
        )[: self.cache_size]
        if len(messages_to_summarize) <= 1:
            return

        history = [
            system("You are a helpful assistant who can summarize conversations."),
            user("Below are the messages you need to summarize."),
            *messages_to_summarize,
            user(
                "Now make an objective summary of the conversation in third person. Only return the summary, no other text."
            ),
        ]

        summary = self.summary_model.run(history).content
        index = self.index(messages_to_summarize[-1])
        self[index].content = textwrap.dedent(
            f"""\
            This is the summary of our previous conversation:
            <summary>
            {summary}
            </summary>
            """
        )
        for i in messages_to_summarize[:-1]:
            self.remove(i)
