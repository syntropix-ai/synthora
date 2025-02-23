import pytest

from synthora.toolkits import AsyncFunction
from synthora.toolkits.base import BaseFunction
from synthora.toolkits.decorators import tool



class TestAsyncFunction:
    def test_decorator(self):
        @tool
        async def add(a: int, b: int) -> int:
            """Add two numbers together"""
            return a + b

        assert add.name == "add"
        assert add.description == "Add two numbers together"
        assert add.parameters == {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}
        assert add.schema == {'type': 'function', 'function': {'name': 'add', 'description': 'Add two numbers together', 'parameters': {'properties': {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}, 'required': ['a', 'b'], 'title': 'add', 'type': 'object'}}}

    def test_wrap(self):
        
        async def add(a: int, b: int) -> int:
            """Add two numbers together"""
            return a + b
        add = BaseFunction.wrap(add)

        assert isinstance(add, AsyncFunction)
        assert add.name == "add"
        assert add.description == "Add two numbers together"
        assert add.parameters == {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}
        assert add.schema == {'type': 'function', 'function': {'name': 'add', 'description': 'Add two numbers together', 'parameters': {'properties': {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}, 'required': ['a', 'b'], 'title': 'add', 'type': 'object'}}}

    async def test_call(self):
        @tool
        async def add(a: int, b: int) -> int:
            """Add two numbers together"""
            return a + b
        
        result = await add(1, 2)
        assert result.is_ok
        assert result.unwrap() == 3
        assert (await add(b=1, a=2)).unwrap() == 3
    
    async def test_call_with_invalid_parameters(self):
        @tool
        async def add(a: int, b: int) -> int:
            """Add two numbers together"""
            return a + b
        
        result = await add(1, "2")
        assert result.is_err
        assert isinstance(result.unwrap_err(), TypeError)
    
    async def test_run(self):
        @tool
        async def add(a: int, b: int) -> int:
            """Add two numbers together"""
            return a + b
        
        result = await add.async_run(1, 2)
        assert result.is_ok
        assert result.unwrap() == 3

    async def test_run_with_invalid_parameters(self):
        @tool
        async def add(a: int, b: int) -> int:
            """Add two numbers together"""
            return a + b
        
        result = await add.async_run(1, "2")
        assert result.is_err
        assert isinstance(result.unwrap_err(), TypeError)

    def test_sync_call(self):
        @tool
        async def add(a: int, b: int) -> int:
            """Add two numbers together"""
            return a + b
        
        with pytest.raises(NotImplementedError):
            add.run(1, 2)

   