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

from copy import deepcopy
from typing import Any, AnyStr, Dict, List, Optional, Type, Union


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from pydantic import BaseModel, model_validator

from synthora.types import (
    ChatCompletion,
    ChatCompletionAssistantMessageParam,
    ChatCompletionChunk,
    ChatCompletionContentPartImageParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionMessageParam,
    ChatCompletionMessageToolCall,
    ChatCompletionSystemMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionUserMessageParam,
)
from synthora.types.enums import MessageRole, NodeType, Result
from synthora.types.node import Node
from synthora.utils.image import parse_image


class BaseMessage(BaseModel):
    """Base message class for handling different types of chat messages.

    Attributes:
        id:
            Message identifier.
        source:
            Source node of the message.
        role:
            Role of the message sender.
        chunk:
            Chunk of streamed message content.
        parsed:
            Parsed message content.
        content:
            Main message content.
        tool_calls:
            Tool calls made in message.
        tool_response:
            Response from tool execution.
        images:
            List of image URLs.
        origional_response:
            Original response from OpenAI.
        metadata:
            Additional message metadata
    """

    id: Optional[str] = None
    source: Node
    role: MessageRole

    chunk: Optional[str] = None
    parsed: Optional[Any] = None
    content: Optional[str] = None
    tool_calls: Optional[List[Any]] = None
    tool_response: Optional[Dict[str, Any]] = None
    images: Optional[List[str]] = None
    origional_response: Optional[
        Union[ChatCompletion, ChatCompletionChunk]
    ] = None

    metadata: Dict[str, Any] = {}

    @model_validator(mode="after")
    def check_empty_message(self) -> Self:
        """Validate that message has at least one content field.

        Returns:
            The validated message instance.

        Raises:
            ValueError:
                If message has no content, images, tool_calls, or
                tool_response.
        """
        if not any(
            getattr(self, field) is not None
            for field in ["content", "tool_calls", "tool_response", "images"]
        ):
            raise ValueError(
                "Message should have at least one of content, images, "
                "tool_calls, tool_response"
            )
        return self

    @property
    def is_complete(self) -> bool:
        """Check if message is complete.

        Returns:
            True if message has a finish reason in metadata.
        """
        return bool(self.metadata.get("finish_reason", ""))

    @property
    def has_tool_calls(self) -> bool:
        """Check if message contains tool calls.

        Returns:
            True if message has tool_calls, False otherwise.
        """
        return bool(self.tool_calls)

    @classmethod
    def create_message(
        cls: Type[Self],
        role: MessageRole,
        id: Optional[str] = None,
        content: Optional[AnyStr] = None,
        images: Optional[List[str]] = None,
        tool_calls: Optional[List[Dict[str, Any]]] = None,
        tool_response: Optional[Result[Dict[str, Any], Exception]] = None,
        source: Optional[Node] = None,
        metadata: Dict[str, Any] = {},
    ) -> Self:
        """Create a new message instance.

        Args:
            role:
                Role of message sender.
            id:
                Message identifier.
            content:
                Message content.
            images:
                List of image URLs.
            tool_calls:
                Tool calls to make.
            tool_response:
                Response from tool execution.
            source:
                Source node, defaults to user.
            metadata:
                Additional metadata.

        Returns:
            New message instance

        Raises:
            ValueError:
                If system message contains images or tool response missing ID.
        """
        if images:
            images = [parse_image(image) for image in images]
        source = source or Node(name="user", type=NodeType.USER)
        if isinstance(content, BaseMessage):
            content = content.content
        match role:
            case MessageRole.USER:
                return cls(
                    source=source or Node(name="user", type=NodeType.USER),
                    role=MessageRole.USER,
                    content=content,
                    images=images,
                    metadata=metadata,
                )
            case MessageRole.SYSTEM:
                if images:
                    raise ValueError("System message cannot have images")
                return cls(
                    source=source or Node(name="system", type=NodeType.SYSTEM),
                    role=MessageRole.SYSTEM,
                    content=content,
                    metadata=metadata,
                )
            case MessageRole.ASSISTANT:
                return cls(
                    source=source
                    or Node(name="assistant", type=NodeType.AGENT),
                    role=MessageRole.ASSISTANT,
                    content=content,
                    tool_calls=tool_calls,
                    images=images,
                    metadata=metadata,
                )
            case MessageRole.TOOL_RESPONSE:
                if id is None:
                    raise ValueError(
                        "Function response message should have an id"
                    )
                return cls(
                    id=id,
                    source=source or Node(name="function", type=NodeType.TOOL),
                    role=MessageRole.TOOL_RESPONSE,
                    content=content,
                    tool_response=tool_response,
                    images=images,
                    metadata=metadata,
                )

    def to_openai_message(self) -> ChatCompletionMessageParam:
        """Convert to OpenAI message format.

        Returns:
            Message in OpenAI format.

        Raises:
            ValueError:
                If system message contains images.
        """
        if self.role == MessageRole.TOOL_RESPONSE:
            return ChatCompletionToolMessageParam(
                content=str(self.content),
                role="tool",
                tool_call_id=self.id,
            )
        else:
            content = self.content
            if self.images:
                content = [  # type: ignore
                    ChatCompletionContentPartTextParam(
                        text=content, type="text"
                    )
                ]
                for image in self.images:
                    content.append(  # type: ignore[union-attr]
                        ChatCompletionContentPartImageParam(
                            image_url={"url": image, "detail": "auto"},
                            type="image_url",
                        )
                    )
            if self.role == MessageRole.USER:
                return ChatCompletionUserMessageParam(
                    content=content,
                    role="user",
                    name=self.source.name,
                )
            elif self.role == MessageRole.SYSTEM:
                if self.images:
                    raise ValueError("System message cannot have images")
                return ChatCompletionSystemMessageParam(
                    content=content,
                    role="system",
                    name=self.source.name,
                )
            elif self.role == MessageRole.ASSISTANT:
                tmp_args = {}
                if self.tool_calls:
                    tmp_args["tool_calls"] = self.tool_calls
                return ChatCompletionAssistantMessageParam(
                    content=content,
                    role="assistant",
                    name=self.source.name,
                    **tmp_args,
                )

    @classmethod
    def from_openai_chat_response(
        cls: Type[Self],
        response: ChatCompletion,
        source: Optional[Node] = None,
    ) -> Self:
        """Create message from OpenAI completion response.

        Args:
            response:
                OpenAI completion response.
            source:
                Source node, defaults to assistant.

        Returns:
            New message instance.
        """
        choice = response.choices[0]
        source = source or Node(name="assistant", type=NodeType.AGENT)
        metadata = {
            "created": response.created,
            "model": response.model,
            "service_tier": getattr(response, "service_tier", None),
            "system_fingerprint": getattr(response, "system_fingerprint", None),
            "usage": response.usage,
            "finish_reason": choice.finish_reason,
        }
        tool_calls = choice.message.tool_calls
        if not tool_calls and getattr(choice.message, "function_call", None):
            tool_calls = [choice.message.function_call]
        try:
            parsed = choice.message.parsed
        except AttributeError:
            parsed = None
        return cls(
            id=response.id,
            source=source,
            role=MessageRole.ASSISTANT,
            content=choice.message.content,
            metadata=metadata,
            tool_calls=tool_calls,
            # origional_response=response,
            parsed=parsed,
        )

    @classmethod
    def from_openai_chat_stream_response(
        cls: Type[Self],
        response: ChatCompletionChunk,
        source: Optional[Node] = None,
        previous: Optional[Self] = None,
    ) -> Self:
        """Create message from OpenAI streaming completion response.

        Args:
            response:
                OpenAI streaming completion chunk.
            source:
                Source node, defaults to assistant.
            previous:
                Previous message instance for content accumulation.

        Returns:
            New or updated message instance with accumulated content.
        """
        choice = response.choices[0]
        source = source or Node(name="assistant", type=NodeType.AGENT)
        metadata = {
            "created": response.created,
            "model": response.model,
            "service_tier": response.service_tier,
            "system_fingerprint": response.system_fingerprint,
            "usage": response.usage,
            "finish_reason": choice.finish_reason,
        }
        if choice.finish_reason and previous:
            item = deepcopy(previous)
            item.metadata.update(metadata)
            item.chunk = None
            return item

        delta = choice.delta
        chunk = delta.content
        previous_tool_calls = previous.tool_calls if previous else []
        if chunk is None:
            tool_calls = delta.tool_calls

            if not tool_calls:
                tool_calls = [delta.function_call]
            for tc in tool_calls:
                if tc.id:
                    previous_tool_calls.append(  # type: ignore[union-attr]
                        ChatCompletionMessageToolCall(
                            **{
                                "id": tc.id,
                                "type": "function",
                                "function": {"name": "", "arguments": ""},
                            }
                        )
                    )
                if function := tc.function:
                    if function.name:
                        chunk = function.name
                        previous_tool_calls[-1].function.name += function.name  # type: ignore[index]
                    if function.arguments:
                        chunk = function.arguments
                        previous_tool_calls[
                            -1
                        ].function.arguments += function.arguments  # type: ignore[index]
        content = previous.content + chunk if previous else chunk
        return cls(
            id=response.id,
            chunk=chunk,
            source=source,
            role=MessageRole.ASSISTANT,
            content=content,
            metadata=metadata,
            tool_calls=previous_tool_calls,
            origional_response=response,
        )
