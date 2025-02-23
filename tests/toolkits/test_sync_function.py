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
        assert add.parameters == {
            "a": {"title": "A", "type": "integer"},
            "b": {"title": "B", "type": "integer"},
        }
        assert add.schema == {
            "type": "function",
            "function": {
                "name": "add",
                "description": "Add two numbers together",
                "parameters": {
                    "properties": {
                        "a": {"title": "A", "type": "integer"},
                        "b": {"title": "B", "type": "integer"},
                    },
                    "required": ["a", "b"],
                    "title": "add",
                    "type": "object",
                },
            },
        }

    def test_wrap(self):
        def add(a: int, b: int) -> int:
            """Add two numbers together"""
            return a + b

        add = BaseFunction.wrap(add)
        assert add.name == "add"
        assert add.description == "Add two numbers together"
        assert add.parameters == {
            "a": {"title": "A", "type": "integer"},
            "b": {"title": "B", "type": "integer"},
        }
        assert add.schema == {
            "type": "function",
            "function": {
                "name": "add",
                "description": "Add two numbers together",
                "parameters": {
                    "properties": {
                        "a": {"title": "A", "type": "integer"},
                        "b": {"title": "B", "type": "integer"},
                    },
                    "required": ["a", "b"],
                    "title": "add",
                    "type": "object",
                },
            },
        }

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
