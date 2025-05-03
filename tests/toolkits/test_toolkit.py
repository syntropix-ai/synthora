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


from synthora.toolkits.base import BaseToolkit
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

    async def test_model_rewrite_bug(self):
        # This test is related to __init__ function of BaseToolkit
        # Fixed by using deepcopy
        # def __init__(self) -> None:
        #     self._exposed_functions = []

        #     for v in self.__class__.__dict__.values():
        #         if isinstance(v, BaseFunction):
        #             if getattr(v, "_flag", False):
        #                 v.instance = self
        #             self._exposed_functions.append(v)
        #
        # If do not use deepcopy, the following test will fail
        # because the message is shared between toolkit instances
        # toolkit will return the same message for all toolkit instances
        #
        # This is a temporary fix
        class MyToolkit(BaseToolkit):
            def __init__(self, message: str):
                super().__init__()
                self.message = message

            @tool
            def hello(self) -> str:
                """Say hello"""
                return self.message

        toolkit = MyToolkit("Hello, world!")
        assert toolkit.hello.run().unwrap() == "Hello, world!"
        toolkit2 = MyToolkit("Hello, world! 2")
        assert toolkit2.hello.run().unwrap() == "Hello, world! 2"
        assert toolkit.hello.run().unwrap() == "Hello, world!"
