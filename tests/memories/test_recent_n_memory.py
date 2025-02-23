import pytest
from synthora.memories.base import BaseMemory
from synthora.memories.full_context_memory import FullContextMemory
from synthora.memories.recent_n_memory import RecentNMemory
from synthora.messages import BaseMessage, user


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
