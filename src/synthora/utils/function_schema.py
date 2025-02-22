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

from inspect import Parameter, signature
from typing import Any, Callable, Dict

from docstring_parser import parse
from pydantic import create_model
from pydantic.fields import FieldInfo


def get_openai_tool_schema(func: Callable[..., Any]) -> Dict[str, Any]:
    """Convert a Python function into an OpenAI tool schema.

    This function analyzes a Python function's signature and docstring to
    generate a compatible OpenAI tool schema for use with OpenAI's function
    calling API.

    Args:
        func:
            The Python function to convert.

    Returns:
        A dictionary containing the OpenAI tool schema with:
            - type: Always "function"
            - function: Dict containing:
                - name: The function name
                - description: From the function's docstring
                - parameters: Parameter schema from function signature

    Example:
        >>> def add(x: int, y: int = 0) -> int:
        ...     '''Add two numbers.'''
        ...     return x + y
        >>> schema = get_openai_tool_schema(add)
    """
    # Initialize dictionary to store parameter information
    fields: Dict[str, Any] = {}

    # Extract parameters from function signature
    for name, p in signature(func).parameters.items():
        # Skip *args and **kwargs parameters
        if (
            p.kind == Parameter.VAR_POSITIONAL
            or p.kind == Parameter.VAR_KEYWORD
        ):
            continue

        # Get parameter type and default value
        fields[name] = (
            p.annotation if p.annotation is not Parameter.empty else Any,
            (
                FieldInfo()
                if p.default is Parameter.empty
                else FieldInfo(default=p.default)
            ),
        )

    # Create Pydantic model from parameters
    model = create_model(func.__name__, **fields)
    paras_schema = model.model_json_schema()

    # Remove 'self' parameter if present (for class methods)
    if "properties" in paras_schema and "self" in paras_schema["properties"]:
        del paras_schema["properties"]["self"]
    if "required" in paras_schema and "self" in paras_schema["required"]:
        paras_schema["required"].remove("self")

    # Handle functions without docstrings
    if not func.__doc__:
        return {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": "",
                "parameters": paras_schema,
            },
        }

    # Parse docstring for parameter descriptions and function description
    docstring = parse(func.__doc__)

    # Add parameter descriptions from docstring
    params = [
        p
        for p in docstring.params
        if p.arg_name in paras_schema["properties"] and p.description
    ]
    for param in params:
        paras_schema["properties"][param.arg_name]["description"] = (
            param.description
        )

    # Combine short and long descriptions from docstring
    description = docstring.short_description or ""
    if docstring.long_description:
        description += f"\n{docstring.long_description}"

    # Create final OpenAI tool schema
    openai_tool_schema = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": description,
            "parameters": paras_schema,
        },
    }
    return openai_tool_schema
