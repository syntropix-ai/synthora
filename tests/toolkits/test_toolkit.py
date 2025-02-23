import pytest

from synthora.toolkits import SyncFunction
from synthora.toolkits.base import BaseFunction, BaseToolkit
from synthora.toolkits.decorators import tool



class TestToolkit:
    async def test_toolkit(self):
        class MyToolkit(BaseToolkit):
            @tool
            def add(self, a: int, b: int) -> int:
                """Add two numbers together"""
                return a + b
            @tool
            async def multiply(self, a: int, b: int) -> int:
                """Multiply two numbers together"""
                return a * b
            @tool
            @staticmethod
            def subtract(a: int, b: int) -> int:
                """Subtract two numbers together"""
                return a - b
            
        toolkit = MyToolkit()
        assert len(toolkit.sync_tools) == 2
        assert len(toolkit.async_tools) == 1
        assert toolkit.sync_tools[0].name == "add"
        assert toolkit.sync_tools[1].name == "subtract"
        assert toolkit.async_tools[0].name == "multiply"

        assert toolkit.add(1, 2).unwrap() == 3
        assert toolkit.subtract(1, 2).unwrap() == -1
        assert (await toolkit.multiply(1, 2)).unwrap() == 2
    
    async def test_toolkit_tools_from_outside(self):
        @tool
        def add(a: int, b: int) -> int:
            """Add two numbers together"""
            return a + b
        
        class MyToolkit(BaseToolkit):
            ADD = add

        toolkit = MyToolkit()
        assert toolkit.sync_tools[0].name == "add"
        assert toolkit.ADD(1, 2).unwrap() == 3

            
