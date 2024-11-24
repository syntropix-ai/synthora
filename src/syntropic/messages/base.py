from pydantic import BaseModel

class MessageSource(BaseModel):
    type: str
    id: str

class BaseMessage(BaseModel):
    source: str