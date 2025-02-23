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
from synthora.memories.recent_n_memory import RecentNMemory
from synthora.messages import user


class TestRecentNMemory:
    def test_inherits_from_base_memory(self):
        assert issubclass(RecentNMemory, BaseMemory)

    def test_init(self):
        memory = RecentNMemory(n=10)
        assert memory.n == 10

    def test_append(self):
        memory = RecentNMemory(n=10)
        for i in range(15):
            memory.append(user(f"Hello, world! {i}"))
            assert len(memory) == min(i + 1, 10)

        assert memory[0].content == "Hello, world! 5"
        assert memory[-1].content == "Hello, world! 14"

    async def test_async_append(self):
        memory = RecentNMemory(n=10)
        for i in range(15):
            await memory.async_append(user(f"Hello, world! {i}"))
            assert len(memory) == min(i + 1, 10)

        assert memory[0].content == "Hello, world! 5"
        assert memory[-1].content == "Hello, world! 14"
