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

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Dict, List, Optional, Union

from synthora.callbacks import get_callback_manager
from synthora.callbacks.base_handler import (
    AsyncCallBackHandler,
    BaseCallBackHandler,
)
from synthora.messages.base import BaseMessage
from synthora.types.enums import ModelBackendType, NodeType
from synthora.types.node import Node


class BaseModelBackend(ABC):
    """Abstract base class for model backends.

    Attributes:
        name (Optional[str]): Name of the model backend
        source (Node): Source node representing the model's context
        model_type (str): Type of the model
        backend_type (ModelBackendType): Type of the backend implementation
        config (Dict[str, Any]): Configuration parameters for the model
        callback_manager: Manager for handling callbacks
    """

    @staticmethod
    @abstractmethod
    def default(
        model_type: Optional[str] = None,
        source: Optional[Node] = None,
        config: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
        handlers: Optional[
            List[Union[BaseCallBackHandler, AsyncCallBackHandler]]
        ] = None,
    ) -> "BaseModelBackend":
        """Return the default model backend."""
        ...

    def __init__(
        self,
        model_type: str,
        source: Node,
        backend_type: ModelBackendType,
        config: Optional[Dict[str, Any]],
        name: Optional[str] = None,
        handlers: Optional[
            List[Union[BaseCallBackHandler, AsyncCallBackHandler]]
        ] = None,
    ) -> None:
        """Initialize the model backend.

        Args:
            model_type (str): Type of the model
            source (Node): Source node for the model
            backend_type (ModelBackendType): Type of backend implementation
            config (Optional[Dict[str, Any]]): Model configuration parameters
            name (Optional[str]): Name of the model backend
            handlers (List[Union[BaseCallBackHandler, AsyncCallBackHandler]]):
                List of callback handlers
        """
        handlers = handlers or []
        self.name = name
        self.source = Node(name=name, type=NodeType.MODEL, ancestor=source)
        self.model_type = model_type
        self.backend_type = backend_type
        self.config = config or {}
        self.callback_manager = get_callback_manager(handlers)
        self.client: Optional[Any] = None
        self.__IGNORE_ON_COPY = ["client"]

    @abstractmethod
    def run(
        self,
        messages: Union[List[BaseMessage], BaseMessage],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Run the model synchronously.

        Args:
            messages (Union[List[BaseMessage], BaseMessage]): Input messages
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            Any: Model output
        """
        ...

    @abstractmethod
    async def async_run(
        self,
        messages: Union[List[BaseMessage], BaseMessage],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Run the model asynchronously.

        Args:
            messages (Union[List[BaseMessage], BaseMessage]): Input messages
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            Any: Model output
        """
        ...

    def add_handler(
        self,
        handler: Union[BaseCallBackHandler, AsyncCallBackHandler],
        recursive: bool = True,
    ) -> None:
        """Add a callback handler to the model.

        Args:
            handler (Union[BaseCallBackHandler, AsyncCallBackHandler]):
                Callback handler to add
            recursive (bool): Whether to add handler recursively
        """
        self.callback_manager.add(handler)

    def __deepcopy__(self, memo: Dict[int, Any]) -> "BaseModelBackend":
        if id(self) in memo:
            return memo[id(self)]  # type: ignore[no-any-return]

        new_obj = self.__class__.__new__(self.__class__)

        memo[id(self)] = new_obj

        for attr, value in self.__dict__.items():
            if attr not in self.__IGNORE_ON_COPY:
                setattr(new_obj, attr, deepcopy(value, memo))
            else:
                setattr(new_obj, attr, None)

        return new_obj

    @property
    def stream(self) -> bool:
        """Return whether the model backend is using streaming output.

        Returns:
            bool: Whether the model backend is using streaming output
        """
        if self.config and "stream" in self.config:
            return bool(self.config["stream"])
        return False

    def set_stream(self, stream: bool) -> None:
        """Set whether the model backend is using streaming output.

        Args:
            stream (bool): Whether the model backend is using streaming output
        """
        if self.config is None:
            self.config = {}
        self.config["stream"] = stream
