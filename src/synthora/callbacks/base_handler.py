from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from synthora.messages.base import BaseMessage
from synthora.types.enums import Result
from synthora.types.node import Node


class BaseCallBackHandler(ABC):

    def on_llm_start(
        self,
        source: Optional[Node],
        messages: List[BaseMessage],
        stream: bool = False,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        pass

    def on_llm_end(
        self,
        source: Optional[Node],
        message: BaseMessage,
        stream: bool = False,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None: 
        pass

    def on_llm_error(
        self,
        source: Optional[Node],
        e: Exception,
        stream: bool = False,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        pass

    def on_llm_chunk(
        self,
        source: Optional[Node],
        message: BaseMessage,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        pass

    def on_tool_start(
        self,
        source: Optional[Node],
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None: 
        pass

    def on_tool_end(
        self,
        source: Optional[Node],
        result: Result[Any, Exception],
    ) -> None: 
        pass

    def on_tool_error(
        self,
        source: Optional[Node],
        result: Result[Any, Exception],
    ) -> None:
        pass

    def on_agent_start(
        self,
        source: Optional[Node],
        message: BaseMessage,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None: 
        pass

    def on_agent_end(
        self,
        source: Optional[Node],
        message: BaseMessage,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None: 
        pass

    def on_agent_error(
        self, source: Optional[Node], e: Exception, *args: Any, **kwargs: Dict[str, Any]
    ) -> None: 
        pass


class AsyncCallBackHandler(BaseCallBackHandler):
    
    async def on_llm_start(
        self,
        source: Optional[Node],
        messages: List[BaseMessage],
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None: 
        pass
    
    async def on_llm_end(
        self,
        source: Optional[Node],
        message: BaseMessage,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None: 
        pass
    
    async def on_llm_error(
        self, source: Optional[Node], e: Exception, *args: Any, **kwargs: Dict[str, Any]
    ) -> None: 
        pass
    
    async def on_llm_chunk(
        self,
        source: Optional[Node],
        message: BaseMessage,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None: 
        pass
    
    async def on_tool_start(
        self,
        source: Optional[Node],
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None: 
        pass
    
    async def on_tool_end(
        self,
        source: Optional[Node],
        result: Result[Any, Exception],
    ) -> None: 
        pass
    
    async def on_tool_error(
        self, source: Optional[Node], result: Result[Any, Exception]
    ) -> None: 
        pass
    
    async def on_agent_start(
        self,
        source: Optional[Node],
        message: List[BaseMessage],
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None: 
        pass
    
    async def on_agent_end(
        self,
        source: Optional[Node],
        message: BaseMessage,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None: 
        pass
    
    async def on_agent_error(
        self, source: Optional[Node], e: Exception, *args: Any, **kwargs: Dict[str, Any]
    ) -> None: 
        pass
