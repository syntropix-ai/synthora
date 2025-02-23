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

from typing import Any, Optional

from synthora.callbacks.base_handler import BaseCallBackHandler
from synthora.messages.base import BaseMessage
from synthora.types.enums import Result
from synthora.types.node import Node


class OutputHandler(BaseCallBackHandler):
    def on_tool_start(
        self, source: Optional[Node], *args: Any, **kwargs: Any
    ) -> None:
        print(
            f"[bold blue]Starting tool: {source.name if source else 'Unknown'}"
        )

    def on_tool_end(
        self, source: Optional[Node], result: Result[Any, Exception]
    ) -> None:
        print(
            f"[cyan] Tool: {source.name if source else 'Unknow'} completed successfully"  # noqa E501
        )

    def on_tool_error(
        self, source: Optional[Node], result: Result[Any, Exception]
    ) -> None:
        print(
            f"[red] Tool: {source.name if source else 'Unknow'} failed with error: {result.unwrap_err_val()}"  # noqa E501
        )

    def on_llm_end(
        self,
        source: Node,
        message: BaseMessage,
        stream: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        print(f"[green]LLM: {source.name} completed successfully")
        print(f"[green]LLM: {message.content}")

    def on_llm_error(
        self,
        source: Node,
        e: Exception,
        stream: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        print(f"[red]LLM: {source.name} failed with error: {e}")

    def on_agent_start(
        self, source: Node, message: BaseMessage, *args: Any, **kwargs: Any
    ) -> None:
        print(
            f"[bold blue]{source.name if source else 'Unknown'}' Task: {message.content}"  # noqa E501
        )

    def on_agent_end(
        self, source: Node, message: BaseMessage, *args: Any, **kwargs: Any
    ) -> None:
        print(
            f"[bold blue]{source.name if source else 'Unknown'}' Response: {message.content}"  # noqa E501
        )

    def on_agent_error(
        self,
        source: Node,
        result: Result[Any, Exception],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        print(
            f"[bold blue]{source.name if source else 'Unknown'}' Error: {result.unwrap_err_val()}"  # noqa E501
        )
