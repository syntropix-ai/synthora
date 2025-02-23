import pytest
from synthora.memories.base import BaseMemory
from synthora.memories.full_context_memory import FullContextMemory
from synthora.messages import BaseMessage, user


class TestFullContextMemory:
    def test_inherits_from_base_memory(self):
        assert issubclass(FullContextMemory, BaseMemory)

    def test_append(self):
        memory = FullContextMemory()
        memory.append(user("Hello, world!"))
        assert len(memory) == 1
        assert memory[0].content == "Hello, world!"

    async def test_async_append(self):
        memory = FullContextMemory()
        await memory.async_append(user("Hello, world!"))
        assert len(memory) == 1
        assert memory[0].content == "Hello, world!"
