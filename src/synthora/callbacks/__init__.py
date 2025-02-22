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

from typing import List, Union

from .base_handler import AsyncCallBackHandler, BaseCallBackHandler
from .base_manager import AsyncCallBackManager, BaseCallBackManager
from .rich_output_handler import RichOutputHandler


def get_callback_manager(
    handlers: List[Union[BaseCallBackHandler, AsyncCallBackHandler]],
) -> Union[BaseCallBackManager, AsyncCallBackManager]:
    """Create an appropriate callback manager based on handler types.

    Creates either a synchronous or asynchronous callback manager depending on
    whether any of the handlers are asynchronous.

    Args:
        handlers (List[Union[BaseCallBackHandler, AsyncCallBackHandler]]):
            List of callback handlers to be managed

    Returns:
        Union[BaseCallBackManager, AsyncCallBackManager]:
            - AsyncCallBackManager if any handlers are async
            - BaseCallBackManager if all handlers are synchronous
    """
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
