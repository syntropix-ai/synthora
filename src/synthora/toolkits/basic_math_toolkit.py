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

from typing import Union

from synthora.toolkits import BaseToolkit
from synthora.toolkits.decorators import tool


class BasicMathToolkit(BaseToolkit):
    r"""A toolkit for basic math operations
    Provides methods for addition, subtraction,
    multiplication, and division
    """

    @tool
    async def async_add(
        self, a: Union[int, float], b: Union[int, float]
    ) -> Union[int, float]:
        r"""Add two numbers together

        Args:
            a (Union[int, float]): The first number
            b (Union[int, float]): The second number

        Returns:
            Union[int, float]: The sum of the two numbers
        """
        return a + b

    @tool
    @staticmethod
    def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        r"""Add two numbers together

        Args:
            a (Union[int, float]): The first number
            b (Union[int, float]): The second number

        Returns:
            Union[int, float]: The sum of the two numbers
        """
        return a + b

    @tool
    @staticmethod
    def subtract(
        a: Union[int, float], b: Union[int, float]
    ) -> Union[int, float]:
        r"""Subtract two numbers

        Args:
            a (Union[int, float]): The first number
            b (Union[int, float]): The second number

        Returns:
            Union[int, float]: The difference of the two numbers
        """
        return a - b

    @tool
    @staticmethod
    def multiply(
        a: Union[int, float], b: Union[int, float]
    ) -> Union[int, float]:
        r"""Multiply two numbers together

        Args:
            a (Union[int, float]): The first number
            b (Union[int, float]): The second number

        Returns:
            Union[int, float]: The product of the two numbers
        """
        return a * b

    @tool
    @staticmethod
    def divide(
        a: Union[int, float], b: Union[int, float]
    ) -> Union[int, float]:
        r"""Divide two numbers

        Args:
            a (Union[int, float]): The first number
            b (Union[int, float]): The second number

        Returns:
            Union[int, float]: The quotient of the two numbers
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b
