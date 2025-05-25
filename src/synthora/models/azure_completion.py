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

from typing import (
    Any,
    AsyncGenerator,
    Dict,
    Generator,
    List,
    Optional,
    Union,
)

from openai import AsyncAzureOpenAI, AzureOpenAI

from synthora.callbacks.base_handler import (
    AsyncCallBackHandler,
    BaseCallBackHandler,
)
from synthora.messages.base import BaseMessage
from synthora.models.openai_chat import OpenAIChatBackend
from synthora.types.enums import CallBackEvent, MessageRole
from synthora.types.node import Node
from synthora.utils.macros import CALL_ASYNC_CALLBACK


class AzureCompletionBackend(OpenAIChatBackend):
    """Azure OpenAI Completion Completion backend implementation.

    Attributes:
        model_type:
            The OpenAI model identifier (e.g., 'gpt-4', 'gpt-3.5-turbo').
        api_key:
            OpenAI API key. Defaults to AZURE_OPENAI_API_KEY env var.
        azure_endpoint:
            Custom API base URL. Defaults to AZURE_OPENAI_ENDPOINT env var.
        api_version:
            Azure OpenAI API version.
                Defaults to AZURE_OPENAI_API_VERSION env var.
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
        azure_endpoint: Optional[str] = None,
        api_version: Optional[str] = None,
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
            azure_endpoint=azure_endpoint,
            api_version=api_version,
            source=source,
            config=config,
            name=name,
            handlers=handlers,
            **kwargs,
        )

    def run(
        self,
        prompt: Union[str, BaseMessage],  # type: ignore[override]
        *args: Any,
        **kwargs: Any,
    ) -> Union[BaseMessage, Generator[BaseMessage, None, None]]:
        """Synchronously generate completions.

        Args:
            prompt:
                The prompt to generate completions from.
            *args:
                Additional positional arguments.
            **kwargs:
                Additional keyword arguments.

        Returns:
            Generated response(s).
            If stream=True, returns a generator of message chunks.
        """
        if not self.client or not isinstance(self.client, AzureOpenAI):
            self.client = AzureOpenAI(**self.kwargs)
        stream = self.config.get("stream", False)
        if isinstance(prompt, str):
            prompt = BaseMessage(
                content=prompt, role=MessageRole.USER, source=self.source
            )
        kwargs["prompt"] = prompt.content
        kwargs["model"] = self.model_type
        kwargs.update(self.config)

        self.callback_manager.call(
            CallBackEvent.LLM_START,
            self.source,
            [prompt],
            stream,
            *args,
            **kwargs,
        )

        try:
            resp = self.client.completions.create(*args, **kwargs)
        except Exception as e:
            self.callback_manager.call(
                CallBackEvent.LLM_ERROR,
                self.source,
                e,
                stream,
                *args,
                **kwargs,
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
                        stream,
                        *args,
                        **kwargs,
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
            result = BaseMessage.from_openai_chat_response(resp, self.source)
            self.callback_manager.call(
                CallBackEvent.LLM_END,
                self.source,
                result,
                stream,
                *args,
                **kwargs,
            )
            return result

    async def async_run(
        self,
        prompt: Union[str, BaseMessage],  # type: ignore[override]
        *args: Any,
        **kwargs: Any,
    ) -> Union[BaseMessage, AsyncGenerator[BaseMessage, None]]:
        """Synchronously generate completions.

        Args:
            messages: Single message or list of messages to process
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            Generated response(s).
            If stream=True, returns a generator of message chunks.
        """
        if not self.client or not isinstance(self.client, AsyncAzureOpenAI):
            self.client = AsyncAzureOpenAI(**self.kwargs)
        stream = self.config.get("stream", False)
        if isinstance(prompt, str):
            prompt = BaseMessage(
                content=prompt, role=MessageRole.USER, source=self.source
            )
        kwargs["prompt"] = prompt.content
        kwargs["model"] = self.model_type
        kwargs.update(self.config)

        CALL_ASYNC_CALLBACK(
            CallBackEvent.LLM_START,
            self.source,
            [prompt],
            stream,
            *args,
            **kwargs,
        )

        try:
            resp = await self.client.completions.create(*args, **kwargs)
        except Exception as e:
            CALL_ASYNC_CALLBACK(
                CallBackEvent.LLM_ERROR,
                self.source,
                e,
                stream,
                *args,
                **kwargs,
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
                        stream,
                        *args,
                        **kwargs,
                    )

                await CALL_ASYNC_CALLBACK(
                    CallBackEvent.LLM_END,
                    self.source,
                    previous_message,
                    stream,
                    *args,
                    **kwargs,
                )

            return stream_messages()
        else:
            result = BaseMessage.from_openai_chat_response(resp, self.source)
            await CALL_ASYNC_CALLBACK(
                CallBackEvent.LLM_END,
                self.source,
                result,
                stream,
                *args,
                **kwargs,
            )
            return result
