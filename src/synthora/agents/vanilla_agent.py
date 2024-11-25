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

import json
from typing import Any, Dict, List, Union, cast

from synthora.agents import BaseAgent
from synthora.configs.agent_config import AgentConfig
from synthora.messages.base import BaseMessage
from synthora.models.base import BaseModelBackend
from synthora.prompts.base import BasePrompt
from synthora.toolkits.base import BaseFunction
from synthora.types.enums import Err, MessageRole, NodeType, Ok, Result
from synthora.types.node import Node


class VanillaAgent(BaseAgent):
    def __init__(
        self,
        config: AgentConfig,
        model: BaseModelBackend,
        prompt: BasePrompt,
        tools: List[Union["BaseAgent", BaseFunction]] = [],
    ) -> None:
        super().__init__(config, model, prompt, tools)
        self.model: BaseModelBackend = (
            self.model[0] if isinstance(self.model, list) else self.model
        )
        self.model.config["tools"] = [tool.schema for tool in tools]
        self.prompt = (
            list(self.prompt.values())[0]
            if isinstance(self.prompt, dict)
            else self.prompt
        )
        self.prompt: BasePrompt = cast(BasePrompt, self.prompt)

    @property
    def schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description or "",
                "parameters": {
                    "properties": {"message": {"title": "Message", "type": "string"}},
                    "required": ["message"],
                    "title": "run",
                    "type": "object",
                },
            },
        }

    def step(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]:
        if args_name := self.prompt.args:
            prompt_args = {}
            for arg in args_name:
                if arg in kwargs:
                    prompt_args[arg] = kwargs[arg]
                elif arg in locals():
                    prompt_args[arg] = locals()[arg]
                elif arg in globals():
                    prompt_args[arg] = globals()[arg]
                else:
                    return Err(
                        Exception(f"Missing argument {arg}"), f"Missing argument {arg}"
                    )
            prompt = self.prompt.format(**prompt_args)
        else:
            prompt = str(self.prompt)
        if not self.history:
            self.history.append(
                BaseMessage.create_message(
                    MessageRole.SYSTEM,
                    content=prompt,
                    source=Node(name=self.name, type=NodeType.SYSTEM),
                )
            )
        else:
            self.history[0].content = prompt

        if isinstance(message, str):
            message = BaseMessage.create_message(
                role=MessageRole.USER,
                content=message,
                source=Node(name="user", type=NodeType.USER),
            )
        if message.content:
            self.history.append(message)
        response = self.model.run(self.history, *args, **kwargs)
        if not isinstance(response, BaseMessage):
            tmp = None
            for res in response:
                tmp = res
            response = tmp
        self.history.append(response)
        return Ok(response)

    def run(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]:
        while True:
            response = self.step(message, *args, **kwargs)
            message = ""
            if response.is_ok:
                data = response.value
                if data.tool_calls:
                    for tool_call in data.tool_calls:
                        func = tool_call.function
                        try:
                            tool = self.get_tool(func.name)
                            tool_args = json.loads(func.arguments)
                            resp = tool.run(**tool_args)
                            self.history.append(
                                BaseMessage.create_message(
                                    id=tool_call.id,
                                    role=MessageRole.TOOL_RESPONSE,
                                    content=resp.value,
                                    source=Node(name=tool.name, type=NodeType.TOOLKIT),
                                )
                            )
                        except Exception as e:
                            self.history.append(
                                BaseMessage.create_message(
                                    id=tool_call.id,
                                    role=MessageRole.TOOL_RESPONSE,
                                    content=f"Error: {str(e)}",
                                    source=Node(name=tool.name, type=NodeType.TOOLKIT),
                                )
                            )

                else:
                    return Ok(data.content)

            else:
                return response

    async def async_run(  # type: ignore[empty-body]
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]:
        pass

    async def async_step(  # type: ignore[empty-body]
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]:
        pass
