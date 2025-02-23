import pytest
from synthora.memories.base import BaseMemory
from synthora.messages import BaseMessage, user


class TestBaseMemory:

    def test_inherits_from_list(self):
        """Test that BaseMemory inherits from list."""
        assert issubclass(BaseMemory, list)

    def test_append(self):
        memory = BaseMemory()
        memory.append(user("Hello, world!"))
        assert len(memory) == 1
        assert memory[0].content == "Hello, world!"


    def test_has_abstract_async_append(self):
        async_append = getattr(BaseMemory, 'async_append', None)
        
        assert async_append is not None
        assert getattr(async_append, '__isabstractmethod__', False)

    def test_accepts_base_message(self):
        from inspect import signature
        
        sig = signature(BaseMemory.async_append)
        message_param = sig.parameters.get('message')
        
        assert message_param is not None
        assert message_param.annotation == BaseMessage

