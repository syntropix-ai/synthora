from typing import List, Union
from .base_handler import BaseCallBackHandler, AsyncCallBackHandler
from .base_manager import BaseCallBackManager, AsyncCallBackManager
from .rich_output_handler import RichOutputHandler


def get_callback_manager(
    handlers: List[Union[BaseCallBackHandler, AsyncCallBackHandler]]
) -> Union[BaseCallBackManager, AsyncCallBackManager]:
    if any(isinstance(handler, AsyncCallBackHandler) for handler in handlers):
        return AsyncCallBackManager(handlers=handlers)
    return BaseCallBackManager(handlers=handlers)


__all__ = [
    "BaseCallBackHandler",
    "AsyncCallBackHandler",
    "BaseCallBackManager",
    "AsyncCallBackManager",
    "RichOutputHandler",
]
