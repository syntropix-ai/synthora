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

import textwrap
from typing import Optional

from synthora.memories.base import BaseMemory
from synthora.memories.full_context_memory import FullContextMemory
from synthora.messages import system, user
from synthora.messages.base import BaseMessage
from synthora.models import BaseModelBackend
from synthora.models.openai_chat import OpenAIChatBackend
from synthora.types.enums import MessageRole


class SummaryMemory(BaseMemory):
    def __init__(
        self,
        n: int = 15,
        cache_size: int = 6,
        summary_model: Optional[BaseModelBackend] = None,
    ) -> None:
        super().__init__()
        self.n = n
        self.cache_size = cache_size
        self.summary_model = summary_model or OpenAIChatBackend.default()

    def append(self, message: BaseMessage) -> None:
        super().append(message)
        if len(self) > self.n:
            self._summarize()

    async def async_append(self, message: BaseMessage) -> None:
        super().append(message)
        if len(self) > self.n:
            await self._async_summarize()

    def _get_history(self, messages: list[BaseMessage]) -> FullContextMemory:
        return FullContextMemory(
            [
                system(
                    "You are a helpful assistant who can summarize "
                    "conversations."
                ),
                user("Below are the messages you need to summarize."),
                *messages,
                user(
                    "Now make an objective summary of the conversation in "
                    "third person. Only return the summary, no other text."
                ),
            ]
        )

    def _update(
        self, summary: str, messages_to_summarize: list[BaseMessage]
    ) -> None:
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

    def _summarize(self) -> None:
        messages_to_summarize = list(
            filter(lambda message: message.role != MessageRole.SYSTEM, self)
        )
        if len(messages_to_summarize) <= 1:
            return
        cursor = min(len(messages_to_summarize), self.cache_size) - 1
        while (
            cursor < len(messages_to_summarize)
            and messages_to_summarize[cursor].role != MessageRole.USER
        ):
            cursor += 1
        messages_to_summarize = messages_to_summarize[: cursor + 1]
        history = self._get_history(messages_to_summarize)

        summary = self.summary_model.run(history).content
        self._update(summary, messages_to_summarize)

    async def _async_summarize(self) -> None:
        messages_to_summarize = list(
            filter(lambda message: message.role != MessageRole.SYSTEM, self)
        )
        if len(messages_to_summarize) <= 1:
            return
        cursor = min(len(messages_to_summarize), self.cache_size) - 1
        while (
            cursor < len(messages_to_summarize)
            and messages_to_summarize[cursor].role != MessageRole.USER
        ):
            cursor += 1
        messages_to_summarize = messages_to_summarize[: cursor + 1]
        history = self._get_history(messages_to_summarize)

        summary = await self.summary_model.async_run(history).content  # type: ignore
        self._update(summary, messages_to_summarize)
