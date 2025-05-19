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

import importlib
import inspect
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, Union


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from synthora.callbacks import get_callback_manager
from synthora.callbacks.base_handler import (
    AsyncCallBackHandler,
    BaseCallBackHandler,
)
from synthora.configs.agent_config import AgentConfig
from synthora.memories.base import BaseMemory
from synthora.memories.full_context_memory import FullContextMemory
from synthora.messages.base import BaseMessage
from synthora.models import create_model_from_config
from synthora.models.base import BaseModelBackend
from synthora.prompts.base import BasePrompt
from synthora.toolkits.base import AsyncFunction, BaseFunction, BaseToolkit
from synthora.types.enums import (
    CallBackEvent,
    NodeType,
    Ok,
    Result,
)
from synthora.types.node import Node
from synthora.utils.macros import CALL_ASYNC_CALLBACK


class BaseAgent(ABC):
    """Base class for all agents.

    This class serves as the foundation for all agent implementations in the
    system. It provides core functionality for:
    - Managing agent configuration and state
    - Handling model interactions
    - Tool management and execution
    - Event callbacks and logging
    - Message history tracking

    Attributes:
        config:
            The configuration settings for the agent.
        source:
            The source node in the computation graph.
        name:
            The name of the agent.
        type:
            The type of the agent.
        description:
            A description of the agent's purpose.
        model:
            The model backend(s).
        prompt:
            The prompt template(s).
        tools:
            Available tools and sub-agents.
        history:
            Message history.
        callback_manager:
            Manages event callbacks.
    """

    @staticmethod
    @abstractmethod
    def default(
        prompt: str,
        name: str = "Base",
        model_type: str = "gpt-4o",
        tools: Optional[List[Union["BaseAgent", BaseFunction]]] = None,
        handlers: Optional[
            List[Union[BaseCallBackHandler, AsyncCallBackHandler]]
        ] = None,
    ) -> "BaseAgent": ...

    def __init__(
        self,
        config: AgentConfig,
        source: Node,
        model: Union[BaseModelBackend, List[BaseModelBackend]],
        prompt: Union[BasePrompt, Dict[str, BasePrompt]],
        tools: Optional[List[Union["BaseAgent", BaseFunction]]] = None,
        handlers: Optional[
            List[Union[BaseCallBackHandler, AsyncCallBackHandler]]
        ] = None,
    ) -> None:
        """Initialize a new agent instance.

        Args:
            config:
                Configuration settings for the agent.
            source:
                The source node in the computation graph.
            model:
                The model backend(s).
            prompt:
                The prompt template(s).
            tools:
                Available tools and sub-agents.
            handlers:
                Callback handlers for monitoring agent events.
        """
        self.config = config
        self.source = source
        self.name = self.config.name
        self.type = self.config.type
        self.description = self.config.description
        self.model = model
        self.prompt = prompt
        self.tools = tools or []
        self.history: BaseMemory = FullContextMemory()
        self.callback_manager = get_callback_manager(handlers or [])
        self.schema = {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description or "",
                "parameters": {
                    "properties": {
                        "message": {"title": "Message", "type": "string"}
                    },
                    "required": ["message"],
                    "title": "run",
                    "type": "object",
                },
            },
        }

    def set_name(self, name: str) -> Self:
        """Set the agent's name.

        Args:
            name:
                The new name for the agent.

        Returns:
            The agent instance.
        """
        self.name = name
        self.schema["function"]["name"] = name  # type: ignore[index]
        return self

    def set_description(self, description: str) -> Self:
        """Set the agent's description.

        Args:
            description:
                The new description for the agent.

        Returns:
            The agent instance.
        """
        self.description = description
        self.schema["function"]["description"] = description  # type: ignore[index]
        return self

    @property
    def parameters(self) -> Dict[str, Any]:
        """Get the parameters schema for this agent.

        Returns:
            A dictionary containing the properties section of the agent's
            function parameters schema
        """
        return self.schema["function"]["parameters"]["properties"]  # type: ignore

    @abstractmethod
    def run(
        self, message: str, *args: Any, **kwargs: Any
    ) -> Result[Any, Exception]:
        """Execute the agent's main synchronous processing logic.

        Args:
            message:
                The input message to process.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            A Result object containing either:
                - The successful execution output (Any type)
                - An Exception if the execution failed
        """
        ...

    @abstractmethod
    async def async_run(
        self, message: str, *args: Any, **kwargs: Any
    ) -> Result[Any, Exception]:
        """Execute the agent's main asynchronous processing logic.

        Args:
            message:
                The input message to process.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            A Result object containing either:
                - The successful execution output (Any type)
                - An Exception if the execution failed
        """
        ...

    @abstractmethod
    def step(
        self, message: str, *args: Any, **kwargs: Any
    ) -> Result[Any, Exception]:
        """Execute a single synchronous step of the agent's processing logic.

        This method represents one iteration of the agent's decision-making
        process.

        Args:
            message:
                The input message to process.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            A Result object containing either:
                - The step execution output (Any type)
                - An Exception if the step failed
        """
        ...

    @abstractmethod
    async def async_step(
        self, message: str, *args: Any, **kwargs: Any
    ) -> Result[Any, Exception]:
        """Execute a single asynchronous step of the agent's processing logic.

        This method represents one iteration of the agent's decision-making
        process.

        Args:
            message:
                The input message to process.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            A Result object containing either:
                - The step execution output (Any type)
                - An Exception if the step failed
        """
        ...

    @classmethod
    def from_config(cls: Type[Self], config: AgentConfig) -> Self:
        """Factory method to create an agent instance from configuration.

        This method handles:
        - Model initialization
        - Tool/toolkit loading and setup
        - Prompt template configuration
        - Node graph construction

        Args:
            config:
                Complete agent configuration including:
                - name: Agent name
                - type: Agent type identifier
                - description: Agent description
                - model: Model configuration(s)
                - prompt: Prompt template(s)
                - tools: Tool configurations

        Returns:
            Fully configured instance of the agent class

        Raises:
            ImportError:
                If tool/toolkit modules cannot be imported.
            ValueError:
                If tool configuration is invalid or missing required fields.
        """
        _model = (
            config.model if isinstance(config.model, list) else [config.model]
        )
        source = Node(name=config.name, type=NodeType.AGENT)
        model = [create_model_from_config(m, source) for m in _model]
        tools: List[Union[BaseFunction, BaseAgent]] = []

        prompt: Union[BasePrompt, Dict[str, BasePrompt]] = {}
        if isinstance(config.prompt, dict):
            for key, value in config.prompt.items():
                prompt[key] = BasePrompt(value)  # type: ignore[index]
        else:
            prompt = BasePrompt(config.prompt)

        for tool in config.tools or []:
            try:
                if "." not in tool.target:
                    module = importlib.import_module(tool.target)
                else:
                    module = importlib.import_module(
                        tool.target.rsplit(".", 1)[0]
                    )
                    module = getattr(module, tool.target.rsplit(".", 1)[1])

                if not inspect.isclass(module):
                    raise ValueError(
                        f"Expected class in module {tool.target}, got "
                        f"{type(module)}"
                    )
                if issubclass(module, BaseToolkit):
                    instance = module(**tool.args)
                    for t in instance.async_tools:
                        t.source.ancestor = source
                    for t in instance.sync_tools:
                        t.source.ancestor = source
                    tools.extend(instance.sync_tools)
                    tools.extend(instance.async_tools)
                elif issubclass(module, BaseAgent):
                    agent_config = AgentConfig.from_dict(tool.args or {})
                    instance = module.from_config(agent_config)  # type: ignore[attr-defined]
                    tools.append(instance)
                elif issubclass(module, BaseFunction):
                    instance = module(**tool.args)
                    instance.source.ancestor = source
                    tools.append(instance)
            except ImportError:
                raise ImportError(f"Could not import {tool.target}")
            except Exception as e:
                raise ValueError(
                    f"Error loading toolkit {tool.target} with args "
                    f"{tool.args}: {e}"
                )
        for t in tools:
            if t.source:
                t.source.ancestor = source
        return cls(
            config=config,
            model=model,  # type: ignore[arg-type]
            prompt=prompt,
            tools=tools,
            source=source,
        )

    def get_tool(self, name: str) -> Union[BaseFunction, "BaseAgent"]:
        """Get a tool by name.

        Args:
            name:
                The name of the tool.

        Returns:
            The tool.

        Raises:
            ValueError:
                If the tool is not found.
        """
        for tool in self.tools:
            if tool.name == name:
                return tool
        raise ValueError(f"Tool {name} not found in agent {self.name}")

    def add_handler(
        self,
        handler: Union[BaseCallBackHandler, AsyncCallBackHandler],
        recursive: bool = True,
    ) -> None:
        """Add a callback to the agent.

        Args:
            handler:
                The callback handler.
            recursive:
                Whether to add the callback recursively to the tools.
        """
        self.callback_manager.add(handler)
        for model in (
            self.model if isinstance(self.model, list) else [self.model]
        ):
            model.add_handler(handler, recursive=recursive)
        for tool in self.tools:
            tool.add_handler(handler, recursive=recursive)

    def call_tool(self, name: str, arguments: str) -> Result[Any, Exception]:
        """Execute a tool by name with the given arguments.

        Args:
            name:
                The name of the tool to execute.
            arguments:
                JSON string containing tool parameters as key-value pairs.

        Returns:
            A Result object where:
                - Success case: Contains tool execution output of any type
                - Error case: Contains Exception with failure details

        Raises:
            ValueError:
                If tool with given name is not found.
            JSONDecodeError:
                If arguments string is not valid JSON.
        """
        tool = self.get_tool(name)
        tool_args = json.loads(arguments)
        return tool.run(**tool_args)

    async def async_call_tool(
        self, name: str, arguments: str
    ) -> Result[Any, Exception]:
        """Execute a tool by name with the given arguments.

        Args:
            name:
                Name of the tool to execute.
            arguments:
                JSON string containing tool parameters as key-value pairs.

        Returns:
            Result object where:
                - Success case: Contains tool execution output of any type
                - Error case: Contains Exception with failure details

        Raises:
            ValueError:
                If tool with given name is not found.
            JSONDecodeError:
                If arguments string is not valid JSON.
        """
        tool = self.get_tool(name)
        tool_args = json.loads(arguments)
        if isinstance(tool, AsyncFunction):
            return await tool.async_run(**tool_args)
        else:
            return tool.run(**tool_args)

    def on_start(
        self,
        message: Union[List[BaseMessage], BaseMessage],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Handle agent start event.

        Triggers appropriate callbacks when the agent starts processing a
        message. If the agent is being used as a tool, also triggers tool start
        callbacks.

        Args:
            message:
                Message or list of messages being processed.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            None
        """
        if self.source.ancestor:
            self.callback_manager.call(
                CallBackEvent.TOOL_START, self.source, message, *args, **kwargs
            )
        self.callback_manager.call(
            CallBackEvent.AGENT_START, self.source, message, *args, **kwargs
        )

    async def async_on_start(
        self,
        message: Union[List[BaseMessage], BaseMessage],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Handle agent start event.

        Triggers appropriate callbacks when the agent starts processing a
        message. If the agent is being used as a tool, also triggers tool start
        callbacks.

        Args:
            message:
                Message or list of messages being processed.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            None
        """
        if self.source.ancestor:
            await CALL_ASYNC_CALLBACK(
                CallBackEvent.TOOL_START, self.source, message, *args, **kwargs
            )
        await CALL_ASYNC_CALLBACK(
            CallBackEvent.AGENT_START, self.source, message, *args, **kwargs
        )

    def on_end(
        self,
        message: BaseMessage,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Handle agent completion event.

        Triggers appropriate callbacks when the agent completes processing.
        If the agent is being used as a tool, also triggers tool completion
        callbacks.

        Args:
            message:
                The final message produced by the agent.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            None
        """
        if self.source.ancestor:
            self.callback_manager.call(
                CallBackEvent.TOOL_END,
                self.source,
                Ok(message.content),
                *args,
                **kwargs,
            )
        self.callback_manager.call(
            CallBackEvent.AGENT_END, self.source, message, *args, **kwargs
        )

    async def async_on_end(
        self,
        message: BaseMessage,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Handle agent completion event.

        Triggers appropriate callbacks when the agent completes processing.
        If the agent is being used as a tool, also triggers tool completion
        callbacks.

        Args:
            message:
                The final message produced by the agent.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            None
        """
        if self.source.ancestor:
            await CALL_ASYNC_CALLBACK(
                CallBackEvent.TOOL_END,
                self.source,
                Ok(message.content),
                *args,
                **kwargs,
            )
        await CALL_ASYNC_CALLBACK(
            CallBackEvent.AGENT_END, self.source, message, *args, **kwargs
        )

    def on_error(
        self,
        result: Result[Any, Exception],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Handle agent error event.

        Triggers appropriate callbacks when the agent encounters an error.
        If the agent is being used as a tool, also triggers tool error
        callbacks.

        Args:
            result:
                Result object containing the error.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            None
        """
        if self.source.ancestor:
            self.callback_manager.call(
                CallBackEvent.TOOL_ERROR, self.source, result, *args, **kwargs
            )
        self.callback_manager.call(
            CallBackEvent.AGENT_ERROR, self.source, result, *args, **kwargs
        )

    async def async_on_error(
        self,
        result: Result[Any, Exception],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Handle agent error event.

        Triggers appropriate callbacks when the agent encounters an error.
        If the agent is being used as a tool, also triggers tool error
        callbacks.

        Args:
            result:
                Result object containing the error.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            None
        """
        if self.source.ancestor:
            await CALL_ASYNC_CALLBACK(
                CallBackEvent.TOOL_ERROR, self.source, result, *args, **kwargs
            )
        await CALL_ASYNC_CALLBACK(
            CallBackEvent.AGENT_ERROR, self.source, result, *args, **kwargs
        )

    def get_compents(
        self, source: Node
    ) -> Optional[Union[Self, BaseFunction, BaseModelBackend, "BaseAgent"]]:
        """Retrieve component by source node.

        Recursively searches through the agent's components (self, models,
        tools) to find the component matching the given source node.

        Args:
            source:
                The source node to search for.

        Returns:
            The matching component if found, None otherwise.
        """
        if source == self.source:
            return self
        for model in (
            self.model if isinstance(self.model, list) else [self.model]
        ):
            if model.source == source:
                return model
        for tool in self.tools:
            if tool.source == source:
                return tool
            if isinstance(tool, BaseAgent):
                comp = tool.get_compents(source)
                if comp:
                    return comp
        return None

    @abstractmethod
    def add_tool(self, tool: Union[BaseFunction, "BaseAgent"]) -> Self:
        """Add a tool to the agent.

        Args:
            tool:
                The tool to add.
        """
        ...

    @abstractmethod
    def remove_tool(self, tool: Union[BaseFunction, "BaseAgent"]) -> Self:
        """Remove a tool from the agent.

        Args:
            tool:
                The tool to remove.
        """
        ...

    def add_tools(self, tools: List[Union[BaseFunction, "BaseAgent"]]) -> Self:
        """Add multiple tools to the agent.

        Args:
            tools:
                The tools to add.
        """
        for tool in tools:
            self.add_tool(tool)
        return self

    @abstractmethod
    def reset(self) -> Self:
        """Reset the agent to its initial state."""
        ...
