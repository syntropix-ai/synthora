import pytest

from synthora.toolkits import SyncFunction
from synthora.toolkits.base import BaseFunction
from synthora.toolkits.decorators import tool



class TestSyncFunction:
    def test_decorator(self):
        @tool
        def add(a: int, b: int) -> int:
            """Add two numbers together"""
            return a + b

        assert add.name == "add"
        assert add.description == "Add two numbers together"
        assert add.parameters == {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}
        assert add.schema == {'type': 'function', 'function': {'name': 'add', 'description': 'Add two numbers together', 'parameters': {'properties': {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}, 'required': ['a', 'b'], 'title': 'add', 'type': 'object'}}}

    def test_wrap(self):
        
        def add(a: int, b: int) -> int:
            """Add two numbers together"""
            return a + b
        add = BaseFunction.wrap(add)
        assert add.name == "add"
        assert add.description == "Add two numbers together"
        assert add.parameters == {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}
        assert add.schema == {'type': 'function', 'function': {'name': 'add', 'description': 'Add two numbers together', 'parameters': {'properties': {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}, 'required': ['a', 'b'], 'title': 'add', 'type': 'object'}}}

    def test_call(self):
        @tool
        def add(a: int, b: int) -> int:
            """Add two numbers together"""
            return a + b
        
        result = add(1, 2)
        assert result.is_ok
        assert result.unwrap() == 3
        assert add(b=1, a=2).unwrap() == 3
    
    def test_call_with_invalid_parameters(self):
        @tool
        def add(a: int, b: int) -> int:
            """Add two numbers together"""
            return a + b
        
        result = add(1, "2")
        assert result.is_err
        assert isinstance(result.unwrap_err(), TypeError)
    
    def test_run(self):
        @tool
        def add(a: int, b: int) -> int:
            """Add two numbers together"""
            return a + b
        
        result = add.run(1, 2)
        assert result.is_ok
        assert result.unwrap() == 3

    def test_run_with_invalid_parameters(self):
        @tool
        def add(a: int, b: int) -> int:
            """Add two numbers together"""
            return a + b
        
        result = add.run(1, "2")
        assert result.is_err
        assert isinstance(result.unwrap_err(), TypeError)

    async def test_async_call(self):
        @tool
        def add(a: int, b: int) -> int:
            """Add two numbers together"""
            return a + b
        with pytest.raises(NotImplementedError):
            await add.async_run(1, 2)
        

   