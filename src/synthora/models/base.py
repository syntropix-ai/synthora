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

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from synthora.callbacks import get_callback_manager
from synthora.callbacks.base_handler import AsyncCallBackHandler, BaseCallBackHandler
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

    def __init__(
        self,
        model_type: str,
        source: Node,
        backend_type: ModelBackendType,
        config: Optional[Dict[str, Any]],
        name: Optional[str] = None,
        handlers: List[Union[BaseCallBackHandler, AsyncCallBackHandler]] = [],
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
        self.name = name
        self.source = Node(name=name, type=NodeType.MODEL, ancestor=source)
        self.model_type = model_type
        self.backend_type = backend_type
        self.config = config or {}
        self.callback_manager = get_callback_manager(handlers)

    @abstractmethod
    def run(
        self,
        messages: Union[List[BaseMessage], BaseMessage],
        *args: Any,
        **kwargs: Dict[str, Any],
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
        **kwargs: Dict[str, Any],
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
