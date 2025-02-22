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

from abc import ABC
from typing import Any, List, Optional, Union

from synthora.callbacks.base_handler import (
    AsyncCallBackHandler,
    BaseCallBackHandler,
)
from synthora.types.enums import CallBackEvent
from synthora.types.node import Node


class BaseCallBackManager(ABC):
    """Base manager for handling callbacks in the system.

    A base class that manages the registration and execution of callback
    handlers.
    Provides functionality to add, remove, and execute callbacks for various
    events.

    Attributes:
        handlers:
            List of registered callback handlers.
        source:
            Source node associated with the callbacks.
    """

    def __init__(
        self, handlers: Optional[List[BaseCallBackHandler]] = None
    ) -> None:
        """Initialize the callback manager.

        Args:
            handlers:
                Initial list of handlers.
        """
        self.handlers = handlers or []
        self.source: Optional[Node] = None

    def to_async(self) -> "AsyncCallBackManager":
        """Convert the callback manager to an asynchronous version.

        Returns:
            AsyncCallBackManager: Asynchronous version of the callback manager
        """
        return AsyncCallBackManager(handlers=self.handlers)

    def to_sync(self) -> "BaseCallBackManager":
        """Convert the callback manager to a synchronous version.

        Returns:
            BaseCallBackManager: Synchronous version of the callback manager
        """

        return self

    def add(self, handler: BaseCallBackHandler) -> None:
        """Add a new callback handler.

        Args:
            handler:
                The handler to be added.

        Raises:
            TypeError: If handler is not of type BaseCallBackHandler.

        """
        if not isinstance(handler, BaseCallBackHandler):
            raise TypeError("Handler must be of type BaseCallBackHandler")
        self.handlers.append(handler)

    def __iadd__(self, handler: BaseCallBackHandler) -> None:
        """Implement the += operator for adding handlers.

        Args:
            handler:
                The handler to be added.
        """
        self.add(handler)

    def remove(self, handler: BaseCallBackHandler) -> bool:
        """Remove a callback handler.

        Args:
            handler:
                The handler to be removed.

        Returns:
            True if handler was found and removed, False otherwise.
        """
        if handler in self.handlers:
            self.handlers.remove(handler)
            return True
        return False

    def __isub__(self, handler: BaseCallBackHandler) -> None:
        """Implement the -= operator for removing handlers.

        Args:
            handler:
                The handler to be removed.
        """
        self.remove(handler)

    def call(self, event: CallBackEvent, *args: Any, **kwargs: Any) -> None:
        """Execute the specified callback event on all handlers.

        Args:
            event:
                The event to be triggered.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        for handler in self.handlers:
            if self.source is not None:
                args = (self.source, *args)
            getattr(handler, event.value)(*args, **kwargs)


class AsyncCallBackManager(BaseCallBackManager):
    """Asynchronous version of the callback manager.

    Extends BaseCallBackManager to support both synchronous and asynchronous
    handlers. Provides asynchronous execution of callbacks while maintaining
    compatibility with synchronous handlers.

    Attributes:
        handlers:
            List of registered handlers.
        source:
            Source node associated with the callbacks.
    """

    def __init__(
        self,
        handlers: List[Union[BaseCallBackHandler, AsyncCallBackHandler]] = [],
    ) -> None:
        """Initialize the async callback manager.

        Args:
            handlers:
                Initial list of handlers. Defaults to empty list.

        Returns:
            None
        """
        self.handlers = handlers
        self.source: Optional[Node] = None

    def to_async(self) -> "AsyncCallBackManager":
        """Convert the callback manager to an asynchronous version.

        Returns:
            Asynchronous version of the callback manager.
        """
        return self

    def to_sync(self) -> "BaseCallBackManager":
        """Convert the callback manager to a synchronous version.

        Returns:
            Synchronous version of the callback manager.
        """
        return BaseCallBackManager(handlers=self.handlers)

    async def call(  # type: ignore[override]
        self, event: CallBackEvent, *args: Any, **kwargs: Any
    ) -> None:
        """Asynchronously execute the specified callback event on all handlers.

        Args:
            event:
                The event to be triggered.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.
        """
        for handler in self.handlers:
            if self.source is not None:
                args = (self.source, *args)
            if isinstance(handler, AsyncCallBackHandler):
                await getattr(handler, event.value)(*args, **kwargs)
            else:
                getattr(handler, event.value)(*args, **kwargs)

    def add(
        self, handler: Union[BaseCallBackHandler, AsyncCallBackHandler]
    ) -> None:
        """Add a new callback handler.

        Args:
            handler:
                The handler to be added.
        """
        self.handlers.append(handler)

    def __iadd__(
        self, handler: Union[BaseCallBackHandler, AsyncCallBackHandler]
    ) -> None:
        """Implement the += operator for adding handlers.

        Args:
            handler:
                The handler to be added.
        """
        self.add(handler)

    def remove(
        self, handler: Union[BaseCallBackHandler, AsyncCallBackHandler]
    ) -> bool:
        """Remove a callback handler.

        Args:
            handler:
                The handler to be removed.

        Returns:
            True if handler was found and removed, False otherwise.
        """
        if handler in self.handlers:
            self.handlers.remove(handler)
            return True
        return False

    def __isub__(
        self, handler: Union[BaseCallBackHandler, AsyncCallBackHandler]
    ) -> None:
        """Implement the -= operator for removing handlers.

        Args:
            handler:
                The handler to be removed.
        """
        self.remove(handler)
