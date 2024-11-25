from abc import ABC
from typing import List, Optional, Union

from synthora.callbacks.base_handler import AsyncCallBackHandler, BaseCallBackHandler
from synthora.types.enums import CallBackEvent
from synthora.types.node import Node


class BaseCallBackManager(ABC):
    def __init__(self, handlers: List[BaseCallBackHandler] = []) -> None:
        self.handlers = handlers
        self.source: Optional[Node] = None
        
    def add(self, handler: BaseCallBackHandler) -> None:
        if not isinstance(handler, BaseCallBackHandler):
            raise TypeError("Handler must be of type BaseCallBackHandler")
        self.handlers.append(handler)
        
    def __iadd__(self, handler: BaseCallBackHandler) -> None:
        self.add(handler)
        
    def remove(self, handler: BaseCallBackHandler) -> bool:
        if handler in self.handlers:
            self.handlers.remove(handler)
            return True
        return False
    
    def __isub__(self, handler: BaseCallBackHandler) -> None:
        self.remove(handler)
        
    def call(self, event: CallBackEvent, *args, **kwargs) -> None:
        for handler in self.handlers:
            if self.source is not None:
                args = (self.source, *args)
            getattr(handler, event.value)(*args, **kwargs)

class AsyncCallBackManager(BaseCallBackManager):

    def __init__(self, handlers: List[Union[BaseCallBackHandler, AsyncCallBackHandler]] = []) -> None:
        self.handlers = handlers
        self.source: Optional[Node] = None

    async def call(self, event: CallBackEvent, *args, **kwargs) -> None:
        for handler in self.handlers:
            if self.source is not None:
                args = (self.source, *args)
            if isinstance(handler, AsyncCallBackHandler):
                await getattr(handler, event.value)(*args, **kwargs)
            else:
                getattr(handler, event.value)(*args, **kwargs)
                
    def add(self, handler: Union[BaseCallBackHandler, AsyncCallBackHandler]) -> None:
        self.handlers.append(handler)
        
    def __iadd__(self, handler: Union[BaseCallBackHandler, AsyncCallBackHandler]) -> None:
        self.add(handler)
        
    def remove(self, handler: Union[BaseCallBackHandler, AsyncCallBackHandler]) -> bool:
        if handler in self.handlers:
            self.handlers.remove(handler)
            return True
        return False
    
    def __isub__(self, handler: Union[BaseCallBackHandler, AsyncCallBackHandler]) -> None:
        self.remove(handler)
