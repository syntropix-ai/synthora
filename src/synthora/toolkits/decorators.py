# LICENSE HEADER MANAGED BY add-license-header
#
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
#

import inspect
from typing import Any, Callable

from synthora.toolkits.base import BaseFunction


def tool(func: Callable[..., Any]) -> BaseFunction:
    """Decorator that marks a function or method as a tool for use in the toolkit system.

    This decorator performs the following:
    1. Inspects the function signature to detect if it's a method (has 'self' parameter)
    2. If it's a method, marks it with a '_flag' attribute for later processing
    3. Wraps the function using BaseFunction.wrap() which creates either a SyncFunction
       or AsyncFunction based on whether the function is async or not

    Args:
        func (Callable[..., Any]): The function or method to be wrapped as a tool.
                                  Can be either sync or async function.

    Returns:
        BaseFunction: A wrapped function that can be either SyncFunction or AsyncFunction,
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
    if parameters and parameters[0].name == "self":
        setattr(func, "_flag", True)
    return BaseFunction.wrap(func)
