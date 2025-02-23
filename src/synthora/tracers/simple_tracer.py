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

from typing import Any, List, cast

from synthora.messages.base import BaseMessage
from synthora.models.base import BaseModelBackend
from synthora.tracers.base import BaseTracer
from synthora.types.enums import CallBackEvent, Result
from synthora.types.event import TraceEvent
from synthora.types.node import Node


class SimpleTracer(BaseTracer):
    """A simple implementation of the BaseTracer that tracks agent execution
    events.

    Implements callback methods for various agent events including agent
    lifecycle, LLM interactions, and tool usage.
    """

    def on_agent_start(
        self, source: Node, message: BaseMessage, *args: Any, **kwargs: Any
    ) -> None:
        """Called when an agent starts processing.

        Args:
            source:
                The node representing the current execution point.
            message:
                The input message being processed.
            *args:
                Variable length argument list.
            **kwargs:
                Arbitrary keyword arguments.

        Raises:
            ValueError: If agent reference is not set
        """
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.append(source)
        self.events.append(
            TraceEvent.create(
                type=CallBackEvent.AGENT_START,
                stack=self.stack,
                data=message,
                current=source,
                metadata={"args": args, "kwargs": kwargs} | message.metadata,
            )
        )

    def on_agent_end(
        self, source: Node, message: BaseMessage, *args: Any, **kwargs: Any
    ) -> None:
        """Called when an agent completes processing.

        Args:
            source:
                The node representing the current execution point.
            message:
                The output message produced.
            *args:
                Variable length argument list.
            **kwargs:
                Arbitrary keyword arguments.

        Raises:
            ValueError: If agent reference is not set
        """
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.pop()
        self.events.append(
            TraceEvent.create(
                type=CallBackEvent.AGENT_END,
                stack=self.stack,
                data=message,
                current=source,
                metadata={"args": args, "kwargs": kwargs} | message.metadata,
            )
        )

    def on_agent_error(
        self,
        source: Node,
        result: Result[Any, Exception],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Called when an agent encounters an error during processing.

        Args:
            source:
                The node representing the current execution point.
            result:
                The error result containing the exception.
            *args:
                Variable length argument list.
            **kwargs:
                Arbitrary keyword arguments.

        Raises:
            ValueError: If agent reference is not set
        """
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.pop()
        self.events.append(
            TraceEvent.create(
                type=CallBackEvent.AGENT_ERROR,
                stack=self.stack,
                data=str(result.unwrap_err_val()),
                metadata={"args": args, "kwargs": kwargs},
                current=source,
            )
        )

    def on_llm_start(
        self,
        source: Node,
        messages: List[BaseMessage],
        stream: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Called when an LLM interaction begins.

        Args:
            source:
                The node representing the LLM component.
            messages:
                The input messages for the LLM.
            stream:
                Whether streaming is enabled. Defaults to False.
            *args:
                Variable length argument list.
            **kwargs:
                Arbitrary keyword arguments.

        Raises:
            ValueError: If agent reference is not set
        """
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.append(source)
        model: BaseModelBackend = cast(
            BaseModelBackend, self.agent.get_compents(source)
        )
        model_type = model.model_type if model else "Unknown"
        self.events.append(
            TraceEvent.create(
                type=CallBackEvent.LLM_START,
                stack=self.stack,
                data=list(messages),
                metadata={
                    "stream": stream,
                    "model": model_type,
                    "args": args,
                    "kwargs": kwargs,
                },
                current=source,
            )
        )

    def on_llm_end(
        self,
        source: Node,
        message: BaseMessage,
        stream: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Called when an LLM interaction completes.

        Args:
            source:
                The node representing the LLM component.
            message:
                The response message from the LLM.
            stream:
                Whether streaming was used. Defaults to False.
            *args:
                Variable length argument list.
            **kwargs:
                Arbitrary keyword arguments.

        Raises:
            ValueError: If agent reference is not set
        """
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.pop()
        model: BaseModelBackend = cast(
            BaseModelBackend, self.agent.get_compents(source)
        )
        model_type = model.model_type if model else "Unknown"
        self.events.append(
            TraceEvent.create(
                type=CallBackEvent.LLM_END,
                stack=self.stack,
                data=message,
                metadata={
                    "stream": stream,
                    "model": model_type,
                    "args": args,
                    "kwargs": kwargs,
                }
                | message.metadata,
                current=source,
            )
        )

    def on_llm_error(
        self,
        source: Node,
        e: Exception,
        stream: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Called when an LLM interaction encounters an error.

        Args:
            source:
                The node representing the LLM component.
            e:
                The exception that occurred during LLM processing.
            stream:
                Whether streaming was being used.
            *args:
                Variable length argument list.
            **kwargs:
                Arbitrary keyword arguments.

        Raises:
            ValueError: If agent reference is not set
        """
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.pop()
        model: BaseModelBackend = cast(
            BaseModelBackend, self.agent.get_compents(source)
        )
        model_type = model.model_type if model else "Unknown"
        self.events.append(
            TraceEvent.create(
                type=CallBackEvent.LLM_ERROR,
                stack=self.stack,
                data=str(e),
                metadata={
                    "stream": stream,
                    "model": model_type,
                    "args": args,
                    "kwargs": kwargs,
                },
                current=source,
            )
        )

    def on_tool_start(self, source: Node, *args: Any, **kwargs: Any) -> None:
        """Called when a tool execution begins.

        Args:
            source:
                The node representing the tool.
            *args:
                Tool input arguments.
            **kwargs:
                Tool keyword arguments.

        Raises:
            ValueError: If agent reference is not set
        """
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.append(source)
        self.events.append(
            TraceEvent.create(
                type=CallBackEvent.TOOL_START,
                stack=self.stack,
                data={"args": args, "kwargs": kwargs},
                metadata={"args": args, "kwargs": kwargs},
                current=source,
            )
        )

    def on_tool_end(
        self,
        source: Node,
        result: Result[Any, Exception],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Called when a tool execution completes successfully.

        Args:
            source:
                The node representing the tool.
            result:
                The result of the tool execution.
            *args:
                Variable length argument list.
            **kwargs:
                Arbitrary keyword arguments.

        Raises:
            ValueError: If agent reference is not set
        """
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.pop()
        self.events.append(
            TraceEvent.create(
                type=CallBackEvent.TOOL_END,
                stack=self.stack,
                data=result,
                metadata={"args": args, "kwargs": kwargs},
                current=source,
            )
        )

    def on_tool_error(
        self,
        source: Node,
        result: Result[Any, Exception],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Called when a tool execution encounters an error.

        Args:
            source:
                The node representing the tool.
            result:
                The error result containing the exception.
            *args:
                Variable length argument list.
            **kwargs:
                Arbitrary keyword arguments.

        Raises:
            ValueError: If agent reference is not set

        Note:
            The error value can be accessed using result.unwrap_err_val()
        """
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.pop()
        self.events.append(
            TraceEvent.create(
                type=CallBackEvent.TOOL_ERROR,
                stack=self.stack,
                data=result.unwrap_err_val(),
                metadata={"args": args, "kwargs": kwargs},
                current=source,
            )
        )
