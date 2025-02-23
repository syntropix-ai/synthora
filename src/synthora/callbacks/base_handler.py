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

from abc import ABC
from typing import Any, List

from synthora.messages.base import BaseMessage
from synthora.types.enums import Result
from synthora.types.node import Node


class BaseCallBackHandler(ABC):
    """Base callback handler for managing various events in the system.

    An abstract base class that defines the interface for handling different
    types of events such as LLM operations, tool executions, and agent
    activities.
    """

    def on_llm_start(
        self,
        source: Node,
        messages: List[BaseMessage],
        stream: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Called when LLM starts processing.

        Args:
            source:
                Source node initiating the LLM operation.
            messages:
                List of messages to be processed.
            stream:
                Whether streaming is enabled. Defaults to False.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        return None

    def on_llm_end(
        self,
        source: Node,
        message: BaseMessage,
        stream: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Called when LLM completes processing.

        Args:
            source:
                Source node that initiated the LLM operation.
            message:
                The final message produced by the LLM.
            stream:
                Whether streaming was enabled. Defaults to False.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        return None

    def on_llm_error(
        self,
        source: Node,
        e: Exception,
        stream: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Called when LLM encounters an error.

        Args:
            source:
                Source node where the error occurred.
            e:
                The exception that was raised.
            stream:
                Whether streaming was enabled. Defaults to False.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        return None

    def on_llm_chunk(
        self,
        source: Node,
        message: BaseMessage,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Called when LLM produces a chunk during streaming.

        Args:
            source:
                Source node producing the chunk.
            message:
                The chunk message.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        return None

    def on_tool_start(
        self,
        source: Node,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Called when a tool starts execution.

        Args:
            source:
                Source node initiating the tool.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        return None

    def on_tool_end(
        self,
        source: Node,
        result: Result[Any, Exception],
    ) -> None:
        """Called when a tool completes execution.

        Args:
            source:
                Source node that executed the tool.
            result:
                The result of the tool execution.
        """
        return None

    def on_tool_error(
        self,
        source: Node,
        result: Result[Any, Exception],
    ) -> None:
        """Called when a tool encounters an error.

        Args:
            source:
                Source node where the error occurred.
            result:
                The error result from the tool.
        """
        return None

    def on_agent_start(
        self,
        source: Node,
        message: BaseMessage,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Called when an agent starts processing.

        Args:
            source:
                Source node initiating the agent.
            message:
                The initial message for the agent.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        return None

    def on_agent_end(
        self,
        source: Node,
        message: BaseMessage,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Called when an agent completes processing.

        Args:
            source:
                Source node of the agent.
            message:
                The final message from the agent.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        return None

    def on_agent_error(
        self,
        source: Node,
        result: Result[Any, Exception],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Called when an agent encounters an error.

        Args:
            source:
                Source node where the error occurred.
            result:
                The error result from the agent.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        return None


class AsyncCallBackHandler(BaseCallBackHandler):
    """Asynchronous version of the callback handler.

    Implements the same interface as BaseCallBackHandler but with async methods
    for handling events in asynchronous contexts.
    """

    async def on_llm_start(  # type: ignore[override]
        self,
        source: Node,
        messages: List[BaseMessage],
        stream: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Async version of on_llm_start.

        Args:
            source:
                Source node initiating the LLM operation.
            messages:
                List of messages to be processed.
            stream:
                Whether streaming is enabled. Defaults to False.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        return None

    async def on_llm_end(  # type: ignore[override]
        self,
        source: Node,
        message: BaseMessage,
        stream: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Async version of on_llm_end.

        Args:
            source:
                Source node that initiated the LLM operation.
            message:
                The final message produced by the LLM.
            stream:
                Whether streaming was enabled. Defaults to False.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        return None

    async def on_llm_error(  # type: ignore[override]
        self,
        source: Node,
        e: Exception,
        stream: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Async version of on_llm_error.

        Args:
            source:
                Source node where the error occurred.
            e:
                The exception that was raised.
            stream:
                Whether streaming was enabled. Defaults to False.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        return None

    async def on_llm_chunk(  # type: ignore[override]
        self,
        source: Node,
        message: BaseMessage,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Async version of on_llm_chunk.

        Args:
            source:
                Source node producing the chunk.
            message:
                The chunk message.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        return None

    async def on_tool_start(  # type: ignore[override]
        self,
        source: Node,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Async version of on_tool_start.

        Args:
            source:
                Source node initiating the tool.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        return None

    async def on_tool_end(  # type: ignore[override]
        self,
        source: Node,
        result: Result[Any, Exception],
    ) -> None:
        """Async version of on_tool_end.

        Args:
            source:
                Source node that executed the tool.
            result:
                The result of the tool execution.
        """
        return None

    async def on_tool_error(  # type: ignore[override]
        self, source: Node, result: Result[Any, Exception]
    ) -> None:
        """Async version of on_tool_error.

        Args:
            source: Source node where the error occurred.
            result: The error result from the tool.
        """
        return None

    async def on_agent_start(  # type: ignore[override]
        self,
        source: Node,
        message: List[BaseMessage],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Async version of on_agent_start.

        Args:
            source:
                Source node initiating the agent.
            message:
                The initial messages for the agent.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        return None

    async def on_agent_end(  # type: ignore[override]
        self,
        source: Node,
        message: BaseMessage,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Async version of on_agent_end.

        Args:
            source:
                Source node of the agent.
            message:
                The final message from the agent.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        return None

    async def on_agent_error(  # type: ignore[override]
        self,
        source: Node,
        result: Result[Any, Exception],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Async version of on_agent_error.

        Args:
            source:
                Source node where the error occurred.
            result:
                The error result from the agent.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        return None
