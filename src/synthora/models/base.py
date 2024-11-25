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
from synthora.types.enums import ModelBackendType


class BaseModelBackend(ABC):
    def __init__(
        self,
        model_type: str,
        backend_type: ModelBackendType,
        config: Optional[Dict[str, Any]],
        name: Optional[str] = None,
        handlers: List[Union[BaseCallBackHandler, AsyncCallBackHandler]] = [],
    ) -> None:
        self.name = name
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
    ) -> Any: ...

    @abstractmethod
    async def async_run(
        self,
        messages: Union[List[BaseMessage], BaseMessage],
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> Any: ...

    def add_handler(
        self,
        handler: Union[BaseCallBackHandler, AsyncCallBackHandler],
        recursive: bool = False,
    ) -> None:
        self.callback_manager.add(handler)
