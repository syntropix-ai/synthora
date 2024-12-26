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

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel

from synthora.types.enums import CallBackEvent
from synthora.types.node import Node


class TraceEvent(BaseModel):
    """A model representing a trace event during agent execution.

    This class captures detailed information about events that occur during
    agent execution, including timing, context, and associated data.

    Attributes:
        id (UUID): Unique identifier for the trace event
        timestamp (float): Unix timestamp when the event occurred
        event_type (CallBackEvent): Type of the callback event (e.g., agent_start, llm_end)
        event_name (Optional[str]): Name of the event, defaults to None
        data (Any): The primary data associated with the event (e.g., messages, results)
        stack (List[Node]): The execution stack at the time of the event
        current (Node): The currently active node when the event occurred
        metadata (Dict[str, Any]): Additional contextual information about the event
    """

    id: UUID
    timestamp: float
    event_type: CallBackEvent
    event_name: Optional[str]

    data: Any
    stack: List[Node]
    current: Node
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the TraceEvent to a dictionary.

        Returns:
            Dict[str, Any]: The TraceEvent as a dictionary.
        """
        data = self.model_dump()
        data["id"] = str(data["id"])
        return data

    @staticmethod
    def create(
        type: CallBackEvent,
        data: Any,
        stack: List[Node],
        current: Node,
        metadata: Dict[str, Any],
    ) -> "TraceEvent":
        """
        Create a new TraceEvent instance.

        Args:
            type (CallBackEvent): The type of the callback event.
            data (Any): The data associated with the event.
            stack (List[Node]): The stack of nodes related to the event.
            metadata (Dict[str, Any]): Additional data for the event.

        Returns:
            TraceEvent: A new instance of TraceEvent.
        """
        return TraceEvent(
            id=uuid.uuid4(),
            timestamp=datetime.now().timestamp(),
            event_type=type,
            event_name=None,
            data=data,
            stack=stack,
            current=current,
            metadata=metadata,
        )
