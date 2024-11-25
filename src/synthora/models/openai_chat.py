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

from synthora.callbacks.base_handler import AsyncCallBackHandler, BaseCallBackHandler
from synthora.messages.base import BaseMessage
from synthora.models.base import BaseModelBackend
from synthora.types.enums import CallBackEvent, ModelBackendType, NodeType
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
        handlers: List[Union[BaseCallBackHandler, AsyncCallBackHandler]] = [],
        **kwargs: Dict[str, Any],
    ) -> None:
        super().__init__(
            model_type=model_type,
            backend_type=ModelBackendType.OPENAI_CHAT,
            config=config,
            name=name,
            handlers=handlers,
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

    def run(
        self,
        messages: Union[List[BaseMessage], BaseMessage],
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> Union[BaseMessage, Generator[BaseMessage, None, None]]:
        if not isinstance(messages, list):
            messages = [messages]
        stream = self.config.get("stream", False)
        self.callback_manager.call(
            CallBackEvent.LLM_START,
            self.source,
            messages,
            stream,
            *args,
            **kwargs,
        )
        messages = [message.to_openai_message() for message in messages]
        try:
            resp = self.client.chat.completions.create(
                messages=messages, model=self.model_type, **self.config
            )
        except Exception as e:
            self.callback_manager.call(
                CallBackEvent.LLM_ERROR, self.source, e, stream, *args, **kwargs
            )
            raise e
        if stream:

            def stream_messages() -> Generator[BaseMessage, None, None]:
                try:
                    previous_message = None
                    for message in resp:
                        previous_message = BaseMessage.from_openai_stream_response(
                            message, self.source, previous_message
                        )
                        self.callback_manager.call(
                            CallBackEvent.LLM_CHUNK,
                            self.source,
                            previous_message,
                            *args,
                            **kwargs,
                        )
                        yield previous_message
                except Exception as e:
                    self.callback_manager.call(
                        CallBackEvent.LLM_ERROR, self.source, e, stream, *args, **kwargs
                    )

                self.callback_manager.call(
                    CallBackEvent.LLM_END,
                    self.source,
                    previous_message,
                    stream,
                    *args,
                    **kwargs,
                )

            return stream_messages()
        else:
            result = BaseMessage.from_openai_response(resp, self.source)
            self.callback_manager.call(
                CallBackEvent.LLM_END, self.source, result, stream, *args, **kwargs
            )
            return result

    @override
    async def async_run(
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
