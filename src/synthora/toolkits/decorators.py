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

import inspect
from typing import Any, Callable

from synthora.toolkits.base import BaseFunction


def tool(func: Callable[..., Any]) -> BaseFunction:
    """Decorator that marks a function or method as a tool for use in the
    toolkit system.

    This decorator will perform the following:
    1. Inspect the function signature to detect if it's a method by checking if
    it has a 'self' parameter.
    2. If it's a method, mark it with a '_flag' attribute for later processing.
    3. Wrap the function using BaseFunction.wrap() which creates either a
    SyncFunction or AsyncFunction based on whether the function is async or
    not.

    Args:
        func:
            The function or method to be wrapped as a tool. Can be either
            sync or async function.

    Returns:
        A wrapped function that can be either SyncFunction or AsyncFunction,
        with additional tool-specific functionality and callback handling.

    Example:
        @tool
        def my_tool(x: int) -> str:
            return str(x)

        class MyToolkit:
            @tool
            def my_method(self, x: int) -> str:
                return str(x)
    """
    signature = inspect.signature(func)
    parameters = list(signature.parameters.values())
    target = BaseFunction.wrap(func)
    if parameters and parameters[0].name == "self":
        setattr(target, "_flag", True)
    return target
