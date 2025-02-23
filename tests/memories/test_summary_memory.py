import pytest
from synthora.memories.base import BaseMemory
from synthora.memories.full_context_memory import FullContextMemory
from synthora.memories.recent_n_memory import RecentNMemory
from synthora.memories.summary_memory import SummaryMemory
from synthora.messages import BaseMessage, user
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
        memory = SummaryMemory(summary_model=OpenAIChatBackend.default(model_type="gpt-4o-mini"))
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
        
        