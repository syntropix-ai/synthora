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

from typing import Any, Dict, List, Optional, cast

from synthora.messages.base import BaseMessage
from synthora.models.base import BaseModelBackend
from synthora.tracers.base import BaseTracer
from synthora.types.enums import CallBackEvent, Result
from synthora.types.event import TraceEvent
from synthora.types.node import Node


class SimpleTracer(BaseTracer):
    def on_agent_start(self, source: Node, message: BaseMessage, *args: Any, **kwargs: Dict[str, Any]) -> None:
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.append(source)
        self.events.append(
            TraceEvent.create(
                type=CallBackEvent.AGENT_START,
                stack=self.stack,
                data=message,
                metadata={"args": args, "kwargs": kwargs} | message.metadata,
            )
        )

    def on_agent_end(self, source: Node, message: BaseMessage, *args: Any, **kwargs: Dict[str, Any]) -> None:
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.pop()
        self.events.append(
            TraceEvent.create(
                type=CallBackEvent.AGENT_END,
                stack=self.stack,
                data=message,
                metadata={"args": args, "kwargs": kwargs} | message.metadata,
            )
        )

    def on_agent_error(self, source: Node, result: Result[Any, Exception], *args: Any, **kwargs: Dict[str, Any]) -> None:
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.pop()
        self.events.append(
            TraceEvent.create(
                type=CallBackEvent.AGENT_ERROR,
                stack=self.stack,
                data=str(result.unwrap_err_val()),
                metadata={"args": args, "kwargs": kwargs},
            )
        )

    def on_llm_start(self, source: Node, messages: List[BaseMessage], stream: bool=False, *args: Any, **kwargs: Dict[str, Any]) -> None:
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.append(source)
        model: BaseModelBackend = cast(BaseModelBackend, self.agent.get_compents(source))
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
            )
        )

    def on_llm_end(self, source: Node, message: BaseMessage, stream: bool=False, *args: Any, **kwargs: Dict[str, Any]) -> None:
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.pop()
        model: BaseModelBackend = cast(BaseModelBackend, self.agent.get_compents(source))
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
                } | message.metadata,
            )
        )

    def on_llm_error(self, source: Node, e: Exception, stream: bool = False, *args: Any, **kwargs: Dict[str, Any]) -> None:
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.pop()
        model: BaseModelBackend = cast(BaseModelBackend, self.agent.get_compents(source))
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
            )
        )

    def on_tool_start(self, source: Node, *args: Any, **kwargs: Dict[str, Any]) -> None:
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.append(source)
        self.events.append(
            TraceEvent.create(
                type=CallBackEvent.TOOL_START,
                stack=self.stack,
                data={"args": args, "kwargs": kwargs},
                metadata={"args": args, "kwargs": kwargs},
            )
        )

    def on_tool_end(self, source: Node, result: Result[Any, Exception], *args: Any, **kwargs: Dict[str, Any]) -> None:
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.pop()
        self.events.append(
            TraceEvent.create(
                type=CallBackEvent.TOOL_END,
                stack=self.stack,
                data=result,
                metadata={"args": args, "kwargs": kwargs},
            )
        )

    def on_tool_error(
        self,
        source: Node,
        result: Result[Any, Exception],
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        if self.agent is None:
            raise ValueError("Agent is not set.")
        self.stack.pop()
        self.events.append(
            TraceEvent.create(
                type=CallBackEvent.TOOL_ERROR,
                stack=self.stack,
                data=result.unwrap_err_val(),
                metadata={"args": args, "kwargs": kwargs},
            )
        )
