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

import pytest

from synthora.memories.base import BaseMemory
from synthora.memories.summary_memory import SummaryMemory
from synthora.messages import user
from synthora.models.openai_chat import OpenAIChatBackend


@pytest.mark.requires_env("OPENAI_API_KEY")
class TestSummaryMemory:
    def test_inherits_from_base_memory(self):
        assert issubclass(SummaryMemory, BaseMemory)

    def test_init(self):
        memory = SummaryMemory()
        assert memory.n == 15
        assert memory.cache_size == 6
        assert isinstance(memory.summary_model, OpenAIChatBackend)

    def test_init_with_custom_model(self):
        memory = SummaryMemory(
            summary_model=OpenAIChatBackend.default(model_type="gpt-4o-mini")
        )
        assert memory.summary_model.model_type == "gpt-4o-mini"

    def test_append(self):
        memory = SummaryMemory()
        memory.append(user("Hello, world!"))
        assert len(memory) == 1
        assert memory[0].content == "Hello, world!"

    async def test_async_append(self):
        memory = SummaryMemory()
        await memory.async_append(user("Hello, world!"))
        assert len(memory) == 1
        assert memory[0].content == "Hello, world!"

    def test_summary(self):
        memory = SummaryMemory(n=2, cache_size=2)
        memory.append(user("Hi, My name is John"))
        memory.append(user("I'm a software engineer"))
        memory.append(user("I'm from San Francisco"))
        assert len(memory) == 2
        assert memory[-1].content == "I'm from San Francisco"

    async def test_async_summary(self):
        memory = SummaryMemory(n=2, cache_size=2)
        memory.append(user("Hi, My name is John"))
        memory.append(user("I'm a software engineer"))
        memory.append(user("I'm from San Francisco"))
        assert len(memory) == 2
        assert memory[-1].content == "I'm from San Francisco"
