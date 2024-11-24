import json
from typing import Any, Dict, List, Union
from synthora.agents import BaseAgent
from synthora.configs.agent_config import AgentConfig
from synthora.messages.base import BaseMessage
from synthora.models.base import BaseModelBackend
from synthora.prompts.base import BasePrompt
from synthora.toolkits.base import BaseToolkit
from synthora.types.enums import Err, MessageRole, NodeType, Ok, Result
from synthora.types.node import Node


class VanillaAgent(BaseAgent):

    def __init__(
        self,
        config: AgentConfig,
        model: BaseModelBackend,
        prompt: BasePrompt,
        tools: List[Union["BaseAgent", BaseToolkit]] = [],
    ) -> None:
        model = model[0] if isinstance(model, list) else model
        model.config["tools"] = [tool.schema for tool in tools]
        prompt = list(prompt.values())[0] if isinstance(prompt, dict) else prompt
        super().__init__(config, model, prompt, tools)

    def step(self, message: Union[str, BaseMessage], *args, **kwargs) -> Result[BaseMessage, Exception]:
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

    def run(self, message: Union[str, BaseMessage], *args, **kwargs) -> Result[Any, Exception]:
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

    async def async_run(self, message: str, *args, **kwargs):
        pass

    async def async_step(self, message: str, *args, **kwargs):
        pass
