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
from synthora.toolkits.base import BaseFunction
from synthora.toolkits.decorators import tool
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


@tool
def finish(response: str) -> str:
    """Stop the conversation and return the final response.

    This tool should only be used when either:
    - A final answer has been determined
    - The problem cannot be solved

    Args:
        response:
            The final response to return

    Returns:
        The unchanged response string
    """
    return response


class ReactAgent(BaseAgent):
    """A ReAct (Reasoning and Acting) agent implementation.

    This agent follows the ReAct pattern of reasoning about actions and
    executing them.
    It can use tools to accomplish tasks and maintains a conversation history.

    Args:
        config:
            Configuration for the agent.
        source:
            Source node for the agent.
        model:
            The underlying model for reasoning.
        prompt:
            The prompt template for the agent.
        tools:
            List of available tools. Defaults to [].
    """

    @staticmethod
    def default(
        prompt: str,
        name: str = "React",
        model_type: str = "gpt-4o",
        tools: Optional[List[Union["BaseAgent", BaseFunction]]] = None,
        handlers: Optional[
            List[Union[BaseCallBackHandler, AsyncCallBackHandler]]
        ] = None,
    ) -> "ReactAgent":
        r"""Create a default ReAct agent with the specified prompt and tools.

        Args:
            prompt:
                The initial prompt for the agent.
            name:
                The name of the agent. Defaults to "React".
            model_type:
                The model type to use. Defaults to "gpt-4o".
            tools:
                List of available tools. Defaults to [].
            handlers:
                List of callback handlers. Defaults to [].

        Returns:
            The created ReAct agent
        """
        tools = tools or []
        handlers = handlers or []
        config = AgentConfig(
            name=name,
            type=AgentType.REACT,
            model=ModelConfig(model_type=model_type, name=model_type),
            prompt=BasePrompt(prompt),
        )
        node = Node(name=name, type=NodeType.AGENT)
        model = create_model_from_config(config.model, node)
        agent = ReactAgent(
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
        self.tools.append(finish)
        self.model.config["tools"] = [tool.schema for tool in tools] + [
            finish.schema
        ]
        self.prompt = (
            list(self.prompt.values())[0]  # type: ignore[attr-defined]
            if isinstance(self.prompt, dict)
            else self.prompt
        )
        self.prompt: BasePrompt = BasePrompt(self.prompt)

    def step(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Any
    ) -> Result[Any, Exception]:
        """Execute a single step of the ReAct agent's reasoning process.

        Updates the system prompt, processes the message, and generates a
        response using the model. Will attempt up to 2 iterations if needed.

        Args:
            message:
                Input message to process.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            A Result containing either:
                - The model's response with potential tool calls
                - An Exception if the step failed
        """
        UPDATE_SYSTEM(prompt=FORMAT_PROMPT())
        for _args in self.prompt.args:
            if _args in kwargs:
                del kwargs[_args]
        message = cast(BaseMessage, STR_TO_USERMESSAGE())
        if message.content:
            self.history.append(message)

        for _ in range(2):
            response = self.model.run(self.history, *args, **kwargs)
            response = GET_FINAL_MESSAGE()
            self.history.append(response)
            if response.tool_calls:
                return Ok(response)
        return Ok(response)

    def run(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Any
    ) -> Result[Any, Exception]:
        """Execute the complete ReAct agent reasoning and action loop.

        Processes the input message and continues executing steps until either:
        - A final answer is reached
        - The 'finish' tool is called
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
                - The final response string
                - An Exception if the execution failed
        """
        message = cast(BaseMessage, STR_TO_USERMESSAGE())
        self.on_start(message)
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
                if tool.name == "finish":
                    data.content = resp_value
                    self.on_end(data)
                    return Ok(resp_value)

    async def async_step(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Any
    ) -> Result[Any, Exception]:
        """Execute a single step of the ReAct agent asynchronously.

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

        for _ in range(2):
            response = await self.model.async_run(
                self.history, *args, **kwargs
            )
            response = await ASYNC_GET_FINAL_MESSAGE()
            await self.history.async_append(response)
            if response.tool_calls:
                return Ok(response)
        return Ok(response)

    async def async_run(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Any
    ) -> Result[Any, Exception]:
        """Execute the ReAct agent loop asynchronously.

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
        await self.async_on_start(message)
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
                if tool.name == "finish":
                    data.content = resp_value
                    await self.async_on_end(data, *args, **kwargs)
                    return Ok(resp_value)

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
