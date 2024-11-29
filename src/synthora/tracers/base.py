from abc import ABC
from typing import List, Optional

from synthora.agents.base import BaseAgent
from synthora.callbacks.base_handler import BaseCallBackHandler
from synthora.types.event import TraceEvent
from synthora.types.node import Node


class BaseTracer(BaseCallBackHandler):
    def __init__(self) -> None:
        self.events: List[TraceEvent] = []
        self.stack: List[Node] = []
        self.agent: Optional[BaseAgent] = None

    def trace(self, agent: BaseAgent) -> None:
        self.agent = agent
        self.agent.add_handler(self)

    def reset(self) -> None:
        self.events.clear()
        self.stack.clear()

class AsyncTracer(BaseTracer):

    async def trace(self, agent: BaseAgent) -> None:  # type: ignore[override]
        self.agent = agent
        self.agent.add_handler(self)

    async def reset(self) -> None: # type: ignore[override]
        self.events.clear()
        self.stack.clear()
