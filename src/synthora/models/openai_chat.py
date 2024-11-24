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

import os
from typing import Any, AsyncGenerator, Dict, Generator, List, Optional, Union, override

from openai import AsyncOpenAI, OpenAI  # type: ignore

from synthora.messages.base import BaseMessage
from synthora.models.base import BaseModelBackend
from synthora.types.enums import ModelBackendType, NodeType
from synthora.types.node import Node


class OpenAIChatBackend(BaseModelBackend):
    def __init__(
        self,
        model_type: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        source: Node = Node(name="assistant", type=NodeType.AGENT),
        config: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        super().__init__(
            model_type=model_type,
            backend_type=ModelBackendType.OPENAI_CHAT,
            config=config,
            name=name,
        )
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.kwargs = kwargs
        if self.api_key is None:
            raise ValueError("API Key is required for OpenAI")
        self.kwargs["api_key"] = self.api_key  # type: ignore[assignment]
        if self.base_url is not None:
            self.kwargs["base_url"] = self.base_url  # type: ignore[assignment]
        self.source = source
        self.client = OpenAI(**self.kwargs)

    def run(  # type: ignore[return]
        self,
        messages: Union[List[BaseMessage], BaseMessage],
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> Union[BaseMessage, Generator[BaseMessage, None, None]]:
        if not isinstance(messages, list):
            messages = [messages]
        messages = [message.to_openai_message() for message in messages]
        resp = self.client.chat.completions.create(
            messages=messages, model=self.model_type, **self.config
        )
        if self.config.get("stream", False):
            def stream_messages():
                previous_message = None
                for message in resp:
                    previous_message = BaseMessage.from_openai_stream_response(
                        message, self.source, previous_message
                    )
                    yield previous_message
            return stream_messages()
        else:
            return BaseMessage.from_openai_response(resp, self.source)

    @override
    async def async_run(  # type: ignore[override]
        self,
        messages: Union[List[BaseMessage], BaseMessage],
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> Union[BaseMessage, AsyncGenerator[BaseMessage, None]]:
        if not isinstance(self.client, AsyncOpenAI):
            self.client = AsyncOpenAI(**self.kwargs)
        if not isinstance(messages, list):
            messages = [messages]
        resp = await self.client.chat.completions.create(
            messages=messages, **self.config
        )
        return BaseMessage.from_openai_response(resp, self.source)
        # if self.config.get("stream", False):
        #     previous_message = None
        #     async for message in resp:
        #         previous_message = BaseMessage.from_openai_stream_response(
        #             message, self.source, previous_message
        #         )
        #         yield previous_message
        # else:
        #     return BaseMessage.from_openai_response(resp, self.source)
