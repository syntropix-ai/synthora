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

import os
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    Generator,
    List,
    Optional,
    Union,
)

from openai import AsyncOpenAI, OpenAI

from synthora.callbacks.base_handler import (
    AsyncCallBackHandler,
    BaseCallBackHandler,
)
from synthora.messages.base import BaseMessage
from synthora.models.base import BaseModelBackend
from synthora.types.enums import CallBackEvent, ModelBackendType, NodeType
from synthora.types.node import Node
from synthora.utils.macros import CALL_ASYNC_CALLBACK


class OpenAIChatBackend(BaseModelBackend):
    """OpenAI Chat Completion backend implementation.

    Attributes:
        model_type:
            The OpenAI model identifier (e.g., 'gpt-4', 'gpt-3.5-turbo').
        api_key:
            OpenAI API key. Defaults to OPENAI_API_KEY env var.
        base_url:
            Custom API base URL. Defaults to OPENAI_BASE_URL env var.
        source:
            Source node for the messages. Defaults to Node(name="assistant",
            type=NodeType.AGENT).
        config:
            Additional configuration parameters. Defaults to None.
        name:
            Backend name identifier. Defaults to None.
        handlers:
            Callback handlers. Defaults to [].
        kwargs:
            Additional keyword arguments for OpenAI client.
    """

    @staticmethod
    def default(  # type: ignore[override]
        model_type: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        source: Optional[Node] = None,
        config: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
        handlers: Optional[
            List[Union[BaseCallBackHandler, AsyncCallBackHandler]]
        ] = None,
        **kwargs: Any,
    ) -> "OpenAIChatBackend":
        r"""Return the default OpenAI Chat model backend."""
        return OpenAIChatBackend(
            model_type=model_type or "gpt-4o",
            api_key=api_key,
            base_url=base_url,
            source=source,
            config=config,
            name=name,
            handlers=handlers,
            **kwargs,
        )

    def __init__(
        self,
        model_type: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        source: Optional[Node] = None,
        config: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
        handlers: Optional[
            List[Union[BaseCallBackHandler, AsyncCallBackHandler]]
        ] = None,
        **kwargs: Any,
    ) -> None:
        source = source or Node(
            name=model_type or "assistant", type=NodeType.AGENT
        )
        handlers = handlers or []
        name = name or source.name
        super().__init__(
            model_type=model_type,
            source=source,
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
        self.kwargs["api_key"] = self.api_key
        if self.base_url is not None:
            self.kwargs["base_url"] = self.base_url
        if isinstance(self.callback_manager, AsyncCallBackHandler):
            self.client = AsyncOpenAI(**self.kwargs)
        else:
            self.client = OpenAI(**self.kwargs)

        # Lazy initialization of the OpenAI client
        # This is done to avoid copy errors when pickling the model backend
        self.client = None

    def run(
        self,
        messages: Union[List[BaseMessage], BaseMessage],
        *args: Any,
        **kwargs: Any,
    ) -> Union[BaseMessage, Generator[BaseMessage, None, None]]:
        """Synchronously generate chat completions.

        Args:
            messages: Single message or list of messages to process
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            Generated response(s).
            If stream=True, returns a generator of message chunks.
        """
        if not self.client or not isinstance(self.client, OpenAI):
            self.client = OpenAI(**self.kwargs)
        if not isinstance(messages, list):
            messages = [messages]
        stream = self.config.get("stream", False)
        messages = [message.to_openai_message() for message in messages]
        kwargs = {**self.config, **kwargs}
        if "tools" in kwargs and not kwargs["tools"]:
            del kwargs["tools"]
        kwargs["model"] = self.model_type
        kwargs["messages"] = messages
        self.callback_manager.call(
            CallBackEvent.LLM_START,
            self.source,
            *args,
            **kwargs,
        )
        try:
            if kwargs.get("response_format", None) is not None:
                resp = self.client.beta.chat.completions.parse(*args, **kwargs)
            else:
                resp = self.client.chat.completions.create(*args, **kwargs)
        except Exception as e:
            self.callback_manager.call(
                CallBackEvent.LLM_ERROR, self.source, e, *args, **kwargs
            )
            raise e
        if stream:

            def stream_messages() -> Generator[BaseMessage, None, None]:
                try:
                    previous_message = None
                    for message in resp:
                        previous_message = (
                            BaseMessage.from_openai_chat_stream_response(
                                message, self.source, previous_message
                            )
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
                        CallBackEvent.LLM_ERROR,
                        self.source,
                        e,
                        # stream,
                        *args,
                        **kwargs,
                    )

                self.callback_manager.call(
                    CallBackEvent.LLM_END,
                    self.source,
                    previous_message,
                    *args,
                    **kwargs,
                )

            return stream_messages()
        else:
            result = BaseMessage.from_openai_chat_response(resp, self.source)
            self.callback_manager.call(
                CallBackEvent.LLM_END, self.source, result, *args, **kwargs
            )
            return result

    async def async_run(
        self,
        messages: Union[List[BaseMessage], BaseMessage],
        *args: Any,
        **kwargs: Any,
    ) -> Union[BaseMessage, AsyncGenerator[BaseMessage, None]]:
        """Asynchronously generate chat completions.

        Args:
            messages: Single message or list of messages to process
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            Generated response(s).
            If stream=True, returns an async generator of message chunks.
        """
        if not self.client or not isinstance(self.client, AsyncOpenAI):
            self.client = AsyncOpenAI(**self.kwargs)
        if not isinstance(messages, list):
            messages = [messages]
        stream = self.config.get("stream", False)
        messages = [message.to_openai_message() for message in messages]
        kwargs = {**self.config, **kwargs}
        kwargs["model"] = self.model_type
        kwargs["messages"] = messages
        if "tools" in kwargs and not kwargs["tools"]:
            del kwargs["tools"]
        await CALL_ASYNC_CALLBACK(
            CallBackEvent.LLM_START,
            self.source,
            *args,
            **kwargs,
        )
        try:
            if kwargs.get("response_format", None) is not None:
                resp = await self.client.beta.chat.completions.parse(
                    *args, **kwargs
                )
            else:
                resp = await self.client.chat.completions.create(
                    *args, **kwargs
                )
        except Exception as e:
            await CALL_ASYNC_CALLBACK(
                CallBackEvent.LLM_ERROR, self.source, e, *args, **kwargs
            )
            raise e
        if stream:

            async def stream_messages() -> AsyncGenerator[BaseMessage, None]:
                try:
                    previous_message = None
                    async for message in resp:
                        previous_message = (
                            BaseMessage.from_openai_chat_stream_response(
                                message, self.source, previous_message
                            )
                        )
                        await CALL_ASYNC_CALLBACK(
                            CallBackEvent.LLM_CHUNK,
                            self.source,
                            previous_message,
                            *args,
                            **kwargs,
                        )

                        yield previous_message
                except Exception as e:
                    await CALL_ASYNC_CALLBACK(
                        CallBackEvent.LLM_ERROR,
                        self.source,
                        e,
                        # stream,
                        *args,
                        **kwargs,
                    )

                await CALL_ASYNC_CALLBACK(
                    CallBackEvent.LLM_END,
                    self.source,
                    previous_message,
                    *args,
                    **kwargs,
                )

            return stream_messages()
        else:
            result = BaseMessage.from_openai_chat_response(resp, self.source)
            await CALL_ASYNC_CALLBACK(
                CallBackEvent.LLM_END, self.source, result, *args, **kwargs
            )
            return result
