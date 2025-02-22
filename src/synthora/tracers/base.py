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

from typing import List, Optional

from synthora.agents.base import BaseAgent
from synthora.callbacks.base_handler import BaseCallBackHandler
from synthora.types.event import TraceEvent
from synthora.types.node import Node


class BaseTracer(BaseCallBackHandler):
    """Base class for tracing agent execution and collecting trace events.

    Attributes:
        events:
            List of trace events collected during execution.
        stack:
            Stack of nodes representing execution context.
        agent:
            Reference to the agent being traced.
    """

    def __init__(self) -> None:
        """Initialize a new BaseTracer instance."""
        self.events: List[TraceEvent] = []
        self.stack: List[Node] = []
        self.agent: Optional[BaseAgent] = None

    def trace(self, agent: BaseAgent) -> None:
        """Start tracing an agent's execution.

        Args:
            agent:
                The agent to trace.
        """
        self.agent = agent
        self.agent.add_handler(self)

    def reset(self) -> None:
        """Reset the tracer state by clearing all events and stack."""
        self.events.clear()
        self.stack.clear()


class AsyncTracer(BaseTracer):
    """Asynchronous version of the BaseTracer for async agent execution."""

    async def trace(self, agent: BaseAgent) -> None:  # type: ignore[override]
        """Start tracing an agent's execution asynchronously.

        Args:
            agent:
                The agent to trace.
        """
        self.agent = agent
        self.agent.add_handler(self)

    async def reset(self) -> None:  # type: ignore[override]
        """Reset the tracer state asynchronously by clearing all events and
        stack.
        """
        self.events.clear()
        self.stack.clear()
