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

from abc import ABC
from typing import Any, Dict, List

from synthora.messages.base import BaseMessage
from synthora.types.enums import Result
from synthora.types.node import Node


class BaseCallBackHandler(ABC):
    def on_llm_start(
        self,
        source: Node,
        messages: List[BaseMessage],
        stream: bool = False,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        return None

    def on_llm_end(
        self,
        source: Node,
        message: BaseMessage,
        stream: bool = False,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        return None

    def on_llm_error(
        self,
        source: Node,
        e: Exception,
        stream: bool = False,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        return None

    def on_llm_chunk(
        self,
        source: Node,
        message: BaseMessage,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        return None

    def on_tool_start(
        self,
        source: Node,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        return None

    def on_tool_end(
        self,
        source: Node,
        result: Result[Any, Exception],
    ) -> None:
        return None

    def on_tool_error(
        self,
        source: Node,
        result: Result[Any, Exception],
    ) -> None:
        return None

    def on_agent_start(
        self,
        source: Node,
        message: BaseMessage,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        return None

    def on_agent_end(
        self,
        source: Node,
        message: BaseMessage,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        return None

    def on_agent_error(
        self,
        source: Node,
        result: Result[Any, Exception],
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        return None


class AsyncCallBackHandler(BaseCallBackHandler):
    async def on_llm_start(  # type: ignore[override]
        self,
        source: Node,
        messages: List[BaseMessage],
        stream: bool = False,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        return None

    async def on_llm_end(  # type: ignore[override]
        self,
        source: Node,
        message: BaseMessage,
        stream: bool = False,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        return None

    async def on_llm_error(  # type: ignore[override]
        self,
        source: Node,
        e: Exception,
        stream: bool = False,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        return None

    async def on_llm_chunk(  # type: ignore[override]
        self,
        source: Node,
        message: BaseMessage,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        return None

    async def on_tool_start(  # type: ignore[override]
        self,
        source: Node,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        return None

    async def on_tool_end(  # type: ignore[override]
        self,
        source: Node,
        result: Result[Any, Exception],
    ) -> None:
        return None

    async def on_tool_error(self, source: Node, result: Result[Any, Exception]) -> None:  # type: ignore[override]
        return None

    async def on_agent_start(  # type: ignore[override]
        self,
        source: Node,
        message: List[BaseMessage],
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        return None

    async def on_agent_end(  # type: ignore[override]
        self,
        source: Node,
        message: BaseMessage,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        return None

    async def on_agent_error(  # type: ignore[override]
        self,
        source: Node,
        result: Result[Any, Exception],
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        return None
