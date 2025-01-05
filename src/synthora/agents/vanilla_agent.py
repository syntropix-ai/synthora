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

from typing import Any, Dict, List, Optional, Union, cast

from synthora.agents import BaseAgent
from synthora.callbacks.base_handler import AsyncCallBackHandler, BaseCallBackHandler
from synthora.configs.agent_config import AgentConfig
from synthora.configs.model_config import ModelConfig
from synthora.messages.base import BaseMessage
from synthora.models import create_model_from_config
from synthora.models.base import BaseModelBackend
from synthora.prompts.base import BasePrompt
from synthora.toolkits.base import BaseFunction
from synthora.types.enums import AgentType, MessageRole, NodeType, Ok, Result
from synthora.types.node import Node
from synthora.utils.macros import (
    ASYNC_GET_FINAL_MESSAGE,
    FORMAT_PROMPT,
    GET_FINAL_MESSAGE,
    STR_TO_USERMESSAGE,
    UPDATE_SYSTEM,
)


class VanillaAgent(BaseAgent):
    """A basic agent implementation with straightforward message processing.

    This agent provides a simple implementation that processes messages sequentially,
    can use tools, and maintains a conversation history.

    Args:
        config (AgentConfig): Configuration for the agent
        source (Node): Source node for the agent
        model (BaseModelBackend): The underlying model for processing
        prompt (BasePrompt): The prompt template for the agent
        tools (List[Union[BaseAgent, BaseFunction]], optional): List of available tools. Defaults to [].
    """

    @staticmethod
    def default(
        prompt: str,
        name: str = "Vanilla",
        model_type: str = "gpt-4o",
        tools: Optional[List[Union["BaseAgent", BaseFunction]]] = None,
        handlers: Optional[
            List[Union[BaseCallBackHandler, AsyncCallBackHandler]]
        ] = None,
    ) -> "VanillaAgent":
        r"""Create a default VanillaAgent instance.

        Args:
            prompt (str): The prompt template for the agent
            name (str, optional): The agent name. Defaults to "Vanilla".
            model_type (str, optional): The model type. Defaults to "gpt-4o".
            tools (List[Union[BaseAgent, BaseFunction]], optional): List of available tools. Defaults to [].
            handlers (List[Union[BaseCallBackHandler, AsyncCallBackHandler]], optional): List of callback handlers. Defaults to [].

        Returns:
            VanillaAgent: A new VanillaAgent instance
        """
        tools, handlers = tools or [], handlers or []
        config = AgentConfig(
            name=name,
            type=AgentType.VANILLA,
            model=ModelConfig(model_type=model_type, name=model_type),
            prompt=BasePrompt(prompt),
            tools=tools,
        )
        node = Node(name=name, type=NodeType.AGENT)
        model = create_model_from_config(config.model, node)  # type: ignore[arg-type]
        agent = VanillaAgent(
            config,
            Node(name=name, type=NodeType.AGENT),
            model,
            config.prompt,  # type: ignore[arg-type]
            config.tools,  # type: ignore[arg-type]
        )
        if handlers:
            for handler in handlers:
                agent.add_handler(handler)

        return agent

    def __init__(
        self,
        config: AgentConfig,
        source: Node,
        model: BaseModelBackend,
        prompt: BasePrompt,
        tools: Optional[List[Union["BaseAgent", BaseFunction]]] = None,
    ) -> None:
        tools = tools or []
        super().__init__(config, source, model, prompt, tools)
        self.model: BaseModelBackend = (
            self.model[0] if isinstance(self.model, list) else self.model
        )
        self.model.config["tools"] = [tool.schema for tool in tools]
        self.prompt = (
            list(self.prompt.values())[0]
            if isinstance(self.prompt, dict)
            else self.prompt
        )

    def step(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]:
        """Execute a single step of message processing.

        Updates the system prompt, processes the input message, and generates a response
        using the model.

        Args:
            message (Union[str, BaseMessage]): Input message to process
            *args (Any): Additional positional arguments
            **kwargs (Dict[str, Any]): Additional keyword arguments

        Returns:
            Result[Any, Exception]: A Result containing either:
                - The model's response
                - An Exception if the step failed
        """
        UPDATE_SYSTEM(prompt=FORMAT_PROMPT())
        message = cast(BaseMessage, STR_TO_USERMESSAGE())
        if message.content:
            self.history.append(message)

        response = self.model.run(self.history, *args, **kwargs)
        response = GET_FINAL_MESSAGE()

        self.history.append(response)
        return Ok(response)

    def run(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]:
        """Execute the complete message processing loop.

        Processes the input message and handles any tool calls that are generated.
        Continues until either:
        - A final response without tool calls is reached
        - An error occurs

        Args:
            message (Union[str, BaseMessage]): Input message to process
            *args (Any): Additional positional arguments
            **kwargs (Dict[str, Any]): Additional keyword arguments

        Returns:
            Result[Any, Exception]: A Result containing either:
                - The final response content
                - An Exception if the execution failed
        """
        message = cast(BaseMessage, STR_TO_USERMESSAGE())
        self.on_start(message, *args, **kwargs)
        while True:
            response = self.step(message, *args, **kwargs)
            message = ""
            if response.is_err:
                self.on_error(response)
                return response

            data = response.unwrap()
            if not data.tool_calls:
                self.on_end(data)
                return Ok(data)

            for tool_call in data.tool_calls:
                func = tool_call.function
                try:
                    tool = self.get_tool(func.name)
                    resp = self.call_tool(func.name, func.arguments)
                    resp_value = resp.unwrap()
                except Exception as e:
                    resp_value = f"Error: {str(e)}"
                    self.on_error(resp)

                self.history.append(
                    BaseMessage.create_message(
                        id=tool_call.id,
                        role=MessageRole.TOOL_RESPONSE,
                        content=resp_value,
                        source=tool.source,
                    )
                )

    async def async_step(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]:
        """Execute a single step of message processing asynchronously.

        Note: This is a placeholder for future async implementation.

        Args:
            message (Union[str, BaseMessage]): Input message to process
            *args (Any): Additional positional arguments
            **kwargs (Dict[str, Any]): Additional keyword arguments

        Returns:
            Result[Any, Exception]: A Result containing either:
                - The step execution result
                - An Exception if the step failed
        """
        UPDATE_SYSTEM(prompt=FORMAT_PROMPT())
        message = cast(BaseMessage, STR_TO_USERMESSAGE())
        if message.content:
            self.history.append(message)

        response = await self.model.async_run(self.history, *args, **kwargs)
        response = await ASYNC_GET_FINAL_MESSAGE()

        self.history.append(response)
        return Ok(response)

    async def async_run(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]:
        """Execute the message processing loop asynchronously.

        Note: This is a placeholder for future async implementation.

        Args:
            message (Union[str, BaseMessage]): Input message to process
            *args (Any): Additional positional arguments
            **kwargs (Dict[str, Any]): Additional keyword arguments

        Returns:
            Result[Any, Exception]: A Result containing either:
                - The final response
                - An Exception if the execution failed
        """
        message = cast(BaseMessage, STR_TO_USERMESSAGE())
        await self.async_on_start(message, *args, **kwargs)
        while True:
            response = await self.async_step(message, *args, **kwargs)
            message = ""
            if response.is_err:
                await self.async_on_error(response, *args, **kwargs)
                return response

            data = response.unwrap()
            if not data.tool_calls:
                await self.async_on_end(data, *args, **kwargs)
                return Ok(data)

            for tool_call in data.tool_calls:
                func = tool_call.function
                try:
                    tool = self.get_tool(func.name)
                    resp = await self.async_call_tool(func.name, func.arguments)
                    resp_value = resp.unwrap()
                except Exception as e:
                    resp_value = f"Error: {str(e)}"
                    await self.async_on_error(resp, *args, **kwargs)

                self.history.append(
                    BaseMessage.create_message(
                        id=tool_call.id,
                        role=MessageRole.TOOL_RESPONSE,
                        content=resp_value,
                        source=tool.source,
                    )
                )
