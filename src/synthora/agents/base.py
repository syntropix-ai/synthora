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

import importlib
import inspect
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Self, Type, Union

from synthora.callbacks import get_callback_manager
from synthora.callbacks.base_handler import AsyncCallBackHandler, BaseCallBackHandler
from synthora.configs.agent_config import AgentConfig
from synthora.messages.base import BaseMessage
from synthora.models import create_model_from_config
from synthora.models.base import BaseModelBackend
from synthora.prompts.base import BasePrompt
from synthora.toolkits.base import BaseFunction, BaseToolkit
from synthora.types.enums import CallBackEvent, NodeType, Ok, Result
from synthora.types.node import Node
from synthora.utils.macros import CALL_ASYNC_CALLBACK


class BaseAgent(ABC):
    """Base class for all agents.

    This class serves as the foundation for all agent implementations in the system.
    It provides core functionality for:
    - Managing agent configuration and state
    - Handling model interactions
    - Tool management and execution
    - Event callbacks and logging
    - Message history tracking

    Attributes:
        config (AgentConfig): The configuration settings for the agent
        source (Node): The source node in the computation graph
        name (str): The name of the agent
        type (str): The type of the agent
        description (str): A description of the agent's purpose
        model (Union[BaseModelBackend, List[BaseModelBackend]]): The model backend(s)
        prompt (Union[BasePrompt, Dict[str, BasePrompt]]): The prompt template(s)
        tools (List[Union[BaseAgent, BaseFunction]]): Available tools and sub-agents
        history (List[BaseMessage]): Message history
        callback_manager (CallbackManager): Manages event callbacks
    """

    def __init__(
        self,
        config: AgentConfig,
        source: Node,
        model: Union[BaseModelBackend, List[BaseModelBackend]],
        prompt: Union[BasePrompt, Dict[str, BasePrompt]],
        tools: List[Union["BaseAgent", BaseFunction]] = [],
        handlers: List[Union[BaseCallBackHandler, AsyncCallBackHandler]] = [],
    ) -> None:
        """Initialize a new agent instance.

        Args:
            config (AgentConfig): Configuration settings for the agent
            source (Node): The source node in the computation graph
            model (Union[BaseModelBackend, List[BaseModelBackend]]): The model backend(s)
            prompt (Union[BasePrompt, Dict[str, BasePrompt]]): The prompt template(s)
            tools (List[Union[BaseAgent, BaseFunction]]): Available tools and sub-agents
            handlers (List[Union[BaseCallBackHandler, AsyncCallBackHandler]]): Callback handlers for monitoring agent events
        """
        self.config = config
        self.source = source
        self.name = self.config.name
        self.type = self.config.type
        self.description = self.config.description
        self.model = model
        self.prompt = prompt
        self.tools = tools
        self.history: List[BaseMessage] = []
        self.callback_manager = get_callback_manager(handlers)

    @property
    def schema(self) -> Dict[str, Any]:
        """Generate the JSON schema describing this agent's interface.

        Returns:

        - Dict[str, Any]: The schema of the agent.
        """
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

    @property
    def parameters(self) -> Dict[str, Any]:
        """Get the parameters schema for this agent.

        Returns:
            Dict[str, Any]: A dictionary containing the properties section of the agent's
                function parameters schema
        """
        return self.schema["function"]["parameters"]["properties"]  # type: ignore[no-any-return]

    @abstractmethod
    def run(
        self, message: str, *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]:
        """Execute the agent's main synchronous processing logic.

        Args:
            message (str): The input message to process
            *args (Any): Additional positional arguments
            **kwargs (Dict[str, Any]): Additional keyword arguments

        Returns:
            Result[Any, Exception]: A Result object containing either:
                - The successful execution output (Any type)
                - An Exception if the execution failed
        """
        ...

    @abstractmethod
    async def async_run(
        self, message: str, *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]:
        """Execute the agent's main asynchronous processing logic.

        Args:
            message (str): The input message to process
            *args (Any): Additional positional arguments
            **kwargs (Dict[str, Any]): Additional keyword arguments

        Returns:
            Result[Any, Exception]: A Result object containing either:
                - The successful execution output (Any type)
                - An Exception if the execution failed
        """
        ...

    @abstractmethod
    def step(
        self, message: str, *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]:
        """Execute a single synchronous step of the agent's processing logic.

        This method represents one iteration of the agent's decision-making process.

        Args:
            message (str): The input message to process
            *args (Any): Additional positional arguments
            **kwargs (Dict[str, Any]): Additional keyword arguments

        Returns:
            Result[Any, Exception]: A Result object containing either:
                - The step execution output (Any type)
                - An Exception if the step failed
        """
        ...

    @abstractmethod
    async def async_step(
        self, message: str, *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]:
        """Execute a single asynchronous step of the agent's processing logic.

        This method represents one iteration of the agent's decision-making process.

        Args:
            message (str): The input message to process
            *args (Any): Additional positional arguments
            **kwargs (Dict[str, Any]): Additional keyword arguments

        Returns:
            Result[Any, Exception]: A Result object containing either:
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
            config (AgentConfig): Complete agent configuration including:
                - name (str): Agent name
                - type (str): Agent type identifier
                - description (str): Agent description
                - model (Union[ModelConfig, List[ModelConfig]]): Model configuration(s)
                - prompt (Union[str, Dict[str, str]]): Prompt template(s)
                - tools (Optional[List[ToolConfig]]): Tool configurations

        Returns:
            Self: Fully configured instance of the agent class

        Raises:
            ImportError: If tool/toolkit modules cannot be imported
            ValueError: If tool configuration is invalid or missing required fields
        """
        _model = config.model if isinstance(config.model, list) else [config.model]
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
                    module = importlib.import_module(tool.target.rsplit(".", 1)[0])
                    module = getattr(module, tool.target.rsplit(".", 1)[1])

                if not inspect.isclass(module):
                    raise ValueError(
                        f"Expected class in module {tool.target}, got {type(module)}"
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
                    f"Error loading toolkit {tool.target} with args {tool.args}: {e}"
                )
        for t in tools:
            if t.source:
                t.source.ancestor = source
        return cls(
            config=config, model=model, prompt=prompt, tools=tools, source=source
        )

    def get_tool(self, name: str) -> Union[BaseFunction, "BaseAgent"]:
        """Get a tool by name.

        Arguments:

        - name: str: The name of the tool.

        Returns:

        - Union[BaseFunction, "BaseAgent"]: The tool.

        Raises:

        - ValueError: If the tool is not found.
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

        Arguments:

        - handler: Union[BaseCallBackHandler, AsyncCallBackHandler]: The callback handler.
        - recursive: bool: Whether to add the callback recursively to the tools.
        """
        self.callback_manager.add(handler)
        for model in self.model if isinstance(self.model, list) else [self.model]:
            model.add_handler(handler, recursive=recursive)
        for tool in self.tools:
            tool.add_handler(handler, recursive=recursive)

    def call_tool(self, name: str, arguments: str) -> Result[Any, Exception]:
        """Execute a tool by name with the given arguments.

        Args:
            name (str): Name of the tool to execute
            arguments (str): JSON string containing tool parameters as key-value pairs

        Returns:
            Result[Any, Exception]: Result object where:
                - Success case: Contains tool execution output of any type
                - Error case: Contains Exception with failure details

        Raises:
            ValueError: If tool with given name is not found
            JSONDecodeError: If arguments string is not valid JSON
        """
        tool = self.get_tool(name)
        tool_args = json.loads(arguments)
        return tool.run(**tool_args)

    async def async_call_tool(
        self, name: str, arguments: str
    ) -> Result[Any, Exception]:
        """Execute a tool by name with the given arguments.

        Args:
            name (str): Name of the tool to execute
            arguments (str): JSON string containing tool parameters as key-value pairs

        Returns:
            Result[Any, Exception]: Result object where:
                - Success case: Contains tool execution output of any type
                - Error case: Contains Exception with failure details

        Raises:
            ValueError: If tool with given name is not found
            JSONDecodeError: If arguments string is not valid JSON
        """
        tool = self.get_tool(name)
        tool_args = json.loads(arguments)
        if isinstance(tool, BaseFunction):
            return tool.run(**tool_args)
        else:
            return await tool.async_run(**tool_args)

    def on_start(
        self,
        message: Union[List[BaseMessage], BaseMessage],
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        """Handle agent start event.

        Triggers appropriate callbacks when the agent starts processing a message.
        If the agent is being used as a tool, also triggers tool start callbacks.

        Args:
            message (Union[List[BaseMessage], BaseMessage]): Message or list of messages being processed
            *args (Any): Additional positional arguments
            **kwargs (Dict[str, Any]): Additional keyword arguments

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
        **kwargs: Dict[str, Any],
    ) -> None:
        """Handle agent start event.

        Triggers appropriate callbacks when the agent starts processing a message.
        If the agent is being used as a tool, also triggers tool start callbacks.

        Args:
            message (Union[List[BaseMessage], BaseMessage]): Message or list of messages being processed
            *args (Any): Additional positional arguments
            **kwargs (Dict[str, Any]): Additional keyword arguments

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
        **kwargs: Dict[str, Any],
    ) -> None:
        """Handle agent completion event.

        Triggers appropriate callbacks when the agent completes processing.
        If the agent is being used as a tool, also triggers tool completion callbacks.

        Args:
            message (BaseMessage): The final message produced by the agent
            *args (Any): Additional positional arguments
            **kwargs (Dict[str, Any]): Additional keyword arguments

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
        **kwargs: Dict[str, Any],
    ) -> None:
        """Handle agent completion event.

        Triggers appropriate callbacks when the agent completes processing.
        If the agent is being used as a tool, also triggers tool completion callbacks.

        Args:
            message (BaseMessage): The final message produced by the agent
            *args (Any): Additional positional arguments
            **kwargs (Dict[str, Any]): Additional keyword arguments

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
        **kwargs: Dict[str, Any],
    ) -> None:
        """Handle agent error event.

        Triggers appropriate callbacks when the agent encounters an error.
        If the agent is being used as a tool, also triggers tool error callbacks.

        Args:
            result (Result[Any, Exception]): Result object containing the error
            *args (Any): Additional positional arguments
            **kwargs (Dict[str, Any]): Additional keyword arguments

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
        **kwargs: Dict[str, Any],
    ) -> None:
        """Handle agent error event.

        Triggers appropriate callbacks when the agent encounters an error.
        If the agent is being used as a tool, also triggers tool error callbacks.

        Args:
            result (Result[Any, Exception]): Result object containing the error
            *args (Any): Additional positional arguments
            **kwargs (Dict[str, Any]): Additional keyword arguments

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

        Recursively searches through the agent's components (self, models, tools)
        to find the component matching the given source node.

        Args:
            source (Node): The source node to search for

        Returns:
            Optional[Union[Self, BaseFunction, BaseModelBackend, "BaseAgent"]]:
                The matching component if found, None otherwise
        """
        if source == self.source:
            return self
        for model in self.model if isinstance(self.model, list) else [self.model]:
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
