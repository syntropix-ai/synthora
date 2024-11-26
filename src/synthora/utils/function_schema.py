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

from inspect import Parameter, signature
from typing import Any, Callable, Dict

from docstring_parser import parse  # type: ignore[import-not-found]
from pydantic import create_model
from pydantic.fields import FieldInfo


def get_openai_tool_schema(func: Callable[..., Any]) -> Dict[str, Any]:
    fields: Dict[str, Any] = {}
    for name, p in signature(func).parameters.items():
        if p.kind == Parameter.VAR_POSITIONAL or p.kind == Parameter.VAR_KEYWORD:
            continue
        fields[name] = (
            p.annotation if p.annotation is not Parameter.empty else Any,
            (
                FieldInfo()
                if p.default is Parameter.empty
                else FieldInfo(default=p.default)
            ),
        )

    model = create_model(func.__name__, **fields)
    paras_schema = model.model_json_schema()

    if "self" in paras_schema["properties"]:
        del paras_schema["properties"]["self"]
    if "self" in paras_schema["required"]:
        paras_schema["required"].remove("self")

    if not func.__doc__:
        return {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": "",
                "parameters": paras_schema,
            },
        }
    docstring = parse(func.__doc__)
    params = [
        p
        for p in docstring.params
        if p.arg_name in paras_schema["properties"] and p.description
    ]
    for param in params:
        paras_schema["properties"][param.arg_name]["description"] = param.description

    description = docstring.short_description or ""
    if docstring.long_description:
        description += f"\n{docstring.long_description}"

    openai_tool_schema = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": description,
            "parameters": paras_schema,
        },
    }
    return openai_tool_schema
