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

from typing import Any, List, Optional, Union, cast


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from synthora.agents import BaseAgent
from synthora.callbacks.base_handler import (
    AsyncCallBackHandler,
    BaseCallBackHandler,
)
from synthora.configs.agent_config import AgentConfig
from synthora.configs.model_config import ModelConfig
from synthora.messages.base import BaseMessage
from synthora.models import create_model_from_config
from synthora.models.base import BaseModelBackend
from synthora.prompts.base import BasePrompt
from synthora.prompts.buildin import VanillaPrompt
from synthora.toolkits.base import BaseFunction
from synthora.types.enums import (
    AgentType,
    Err,
    MessageRole,
    NodeType,
    Ok,
    Result,
)
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

    This agent provides a simple implementation that processes messages
    sequentially, can use tools, and maintains a conversation history.

    Args:
        config:
            Configuration for the agent.
        source:
            Source node for the agent.
        model:
            The underlying model for processing.
        prompt:
            The prompt template for the agent.
        tools:
            List of available tools. Defaults to [].
    """

    @staticmethod
    def default(
        prompt: str = VanillaPrompt,
        name: str = "Vanilla",
        model_type: str = "gpt-4o",
        tools: Optional[List[Union["BaseAgent", BaseFunction]]] = None,
        handlers: Optional[
            List[Union[BaseCallBackHandler, AsyncCallBackHandler]]
        ] = None,
    ) -> "VanillaAgent":
        r"""Create a default VanillaAgent instance.

        Args:
            prompt:
                The prompt template for the agent.
            name:
                The agent name.
            model_type:
                The model type.
            tools:
                List of available tools.
            handlers:
                List of callback handlers.

        Returns:
            VanillaAgent: A new VanillaAgent instance
        """
        tools, handlers = tools or [], handlers or []
        config = AgentConfig(
            name=name,
            type=AgentType.VANILLA,
            model=ModelConfig(model_type=model_type, name=model_type),
            prompt=BasePrompt(prompt),
        )
        node = Node(name=name, type=NodeType.AGENT)
        model = create_model_from_config(config.model, node)
        agent = VanillaAgent(
            config,
            Node(name=name, type=NodeType.AGENT),
            model,  # type: ignore[arg-type]
            config.prompt,  # type: ignore[arg-type]
            tools,
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
            list(self.prompt.values())[0]  # type: ignore[attr-defined]
            if isinstance(self.prompt, dict)
            else self.prompt
        )
        self.prompt: BasePrompt = BasePrompt(self.prompt)

    def step(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Any
    ) -> Result[Any, Exception]:
        """Execute a single step of message processing.

        Updates the system prompt, processes the input message, and generates a
        response using the model.

        Args:
            message:
                Input message to process.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            A Result containing either:
                - The model's response
                - An Exception if the step failed
        """
        UPDATE_SYSTEM(prompt=FORMAT_PROMPT())
        for _args in self.prompt.args:
            if _args in kwargs:
                del kwargs[_args]
        message = cast(BaseMessage, STR_TO_USERMESSAGE())
        if message.content:
            self.history.append(message)

        response = self.model.run(self.history, *args, **kwargs)
        response = GET_FINAL_MESSAGE()

        self.history.append(response)
        return Ok(response)

    def run(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Any
    ) -> Result[Any, Exception]:
        """Execute the complete message processing loop.

        Processes the input message and handles any tool calls that are
        generated.
        Continues until either:
        - A final response without tool calls is reached
        - An error occurs

        Args:
            message:
                Input message to process.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            A Result containing either:
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
                    try:
                        self.on_error(resp)
                    except Exception as _:
                        self.on_error(Err(e, resp_value))

                self.history.append(
                    BaseMessage.create_message(
                        id=tool_call.id,
                        tool_response=resp_value,
                        role=MessageRole.TOOL_RESPONSE,
                        content=str(resp_value),
                        source=tool.source,
                    )
                )

    async def async_step(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Any
    ) -> Result[Any, Exception]:
        """Execute a single step of message processing asynchronously.

        Note: This is a placeholder for future async implementation.

        Args:
            message:
                Input message to process.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            A Result containing either:
                - The step execution result
                - An Exception if the step failed
        """
        UPDATE_SYSTEM(prompt=FORMAT_PROMPT())
        for _args in self.prompt.args:
            del kwargs[_args]
        message = cast(BaseMessage, STR_TO_USERMESSAGE())
        if message.content:
            await self.history.async_append(message)

        response = await self.model.async_run(self.history, *args, **kwargs)
        response = await ASYNC_GET_FINAL_MESSAGE()

        await self.history.async_append(response)
        return Ok(response)

    async def async_run(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Any
    ) -> Result[Any, Exception]:
        """Execute the message processing loop asynchronously.

        Note: This is a placeholder for future async implementation.

        Args:
            message:
                Input message to process.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            A Result containing either:
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
                    resp = await self.async_call_tool(
                        func.name, func.arguments
                    )
                    resp_value = resp.unwrap()
                except Exception as e:
                    resp_value = f"Error: {str(e)}"
                    await self.async_on_error(resp, *args, **kwargs)

                await self.history.async_append(
                    BaseMessage.create_message(
                        id=tool_call.id,
                        tool_response=resp_value,
                        role=MessageRole.TOOL_RESPONSE,
                        content=str(resp_value),
                        source=tool.source,
                    )
                )

    def add_tool(self, tool: Union["BaseAgent", BaseFunction]) -> Self:
        """Add a tool to the agent's toolset.

        Args:
            tool:
                The tool to add.

        Returns:
            The agent instance.
        """
        self.tools.append(tool)
        self.model.config["tools"].append(tool.schema)
        return self

    def remove_tool(self, tool: Union["BaseAgent", BaseFunction]) -> Self:
        """Remove a tool from the agent's toolset.

        Args:
            tool:
                The tool to remove.

        Returns:
            The agent instance.
        """
        self.tools.remove(tool)
        self.model.config["tools"].remove(tool.schema)
        return self

    def reset(self) -> Self:
        """Reset the agent's state.

        Returns:
            The agent instance.
        """
        self.history.clear()
        return self
