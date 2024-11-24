from typing import Optional
from pydantic import BaseModel
from synthora.types.enums import NodeType


class Node(BaseModel):
    name: str
    type: NodeType
    ancestor: Optional["Node"] = None
