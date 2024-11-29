from typing import Any, Dict, List
from uuid import UUID
import uuid
from pydantic import BaseModel

from synthora.types.enums import CallBackEvent
from synthora.types.node import Node
from datetime import datetime


class TraceEvent(BaseModel):
    id: UUID
    timestamp: float
    event_type: CallBackEvent

    data: Any
    stack: List[Node]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the TraceEvent to a dictionary.

        Returns:
            Dict[str, Any]: The TraceEvent as a dictionary.
        """
        data = self.model_dump()
        data['id'] = str(data['id'])
        return data
    
    @staticmethod
    def create(
        type: CallBackEvent,
        data: Any,
        stack: List[Node],
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
            data=data,
            stack=stack,
            metadata=metadata,
        )
