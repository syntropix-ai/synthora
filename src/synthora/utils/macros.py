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

import inspect
from typing import Any, Callable, Dict, List, Optional, Union

from synthora.callbacks.base_manager import (
    AsyncCallBackManager,
    BaseCallBackManager,
)
from synthora.messages.base import BaseMessage
from synthora.prompts.base import BasePrompt
from synthora.types.enums import MessageRole, NodeType
from synthora.types.node import Node


def macro(func: Callable[..., Any]) -> Callable[..., Any]:
    r"""A decorator to create a macro function.

    Macro functions can access the local variables of the caller function.
    """
    if inspect.iscoroutinefunction(func):

        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            caller_frame = inspect.currentframe().f_back  # type: ignore[union-attr]
            caller_locals = caller_frame.f_locals  # type: ignore[union-attr]
            kwargs["__macro_locals__"] = caller_locals
            return await func(*args, **kwargs)

        return async_wrapper
    else:

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            caller_frame = inspect.currentframe().f_back  # type: ignore[union-attr]
            caller_locals = caller_frame.f_locals  # type: ignore[union-attr]
            kwargs["__macro_locals__"] = caller_locals
            return func(*args, **kwargs)

        return wrapper


@macro
def FORMAT_PROMPT(
    prompt: Optional[Union[BasePrompt, Dict[str, BasePrompt]]] = None,
    **kwargs: Any,
) -> Union[BasePrompt, Dict[str, BasePrompt]]:
    r"""Format the prompt.

    Args:
        prompt:
            The prompt to format.
        kwargs:
            Dict[str, Any]: The local variables of the caller function.

    Returns:
        The formatted prompt.

    """
    if prompt is None:
        prompt = kwargs.get("__macro_locals__").get("self").prompt  # type: ignore[union-attr]
    params = {
        **kwargs,
        **globals(),
        **kwargs.get("__macro_locals__").get("kwargs", {}),  # type: ignore[union-attr]
    }
    if "self" in params:
        del params["self"]
    if isinstance(prompt, dict):
        return {k: v.format(**params) for k, v in prompt.items()}
    return prompt.format(**params)


@macro
def UPDATE_SYSTEM(
    history: Optional[List[BaseMessage]] = None,
    prompt: Optional[BasePrompt] = None,
    source: Optional[Node] = None,
    **kwargs: Any,
) -> None:
    r"""Update the system message.

    Args:
        history:
            The history of the agent.
        prompt:
            The prompt of the agent.
        source:
            The source node of the agent.
        kwargs:
            Dict[str, Any]: The local variables of the caller function.
    """
    if not history:
        history = kwargs.get("__macro_locals__").get("self").history  # type: ignore[union-attr]
    if not prompt:
        prompt = kwargs.get("__macro_locals__").get("self").prompt  # type: ignore[union-attr]
    if not source:
        source = kwargs.get("__macro_locals__").get("self").source  # type: ignore[union-attr]
    name = (
        kwargs.get("name", None)
        or kwargs.get("__macro_locals__", {}).get("self").name
    )
    if not history:
        history.append(  # type: ignore[union-attr]
            BaseMessage.create_message(
                MessageRole.SYSTEM,
                content=prompt,
                source=Node(name=name, type=NodeType.SYSTEM, ancestor=source),
            )
        )
    else:
        if history[0].role == MessageRole.SYSTEM:
            history[0].content = prompt
        else:
            for i, message in enumerate(history):
                if message.role == MessageRole.SYSTEM:
                    history[i].content = prompt
                    return
            history.insert(
                0,
                BaseMessage.create_message(
                    MessageRole.SYSTEM,
                    content=prompt,
                    source=Node(
                        name=name, type=NodeType.SYSTEM, ancestor=source
                    ),
                ),
            )


@macro
def STR_TO_USERMESSAGE(
    message: Optional[Union[str, BaseMessage]] = None,
    **kwargs: Any,
) -> BaseMessage:
    r"""Convert a string to a user message.
    if the input is a string, it will be converted to a user message.
    otherwise, it will be returned as is.

    Args:
        message:
            The message to convert.
        kwargs:
            Dict[str, Any]: The local variables of the caller function.

    Returns:
        The user message.

    """
    if message is None:
        message = kwargs.get("__macro_locals__", {}).get("message")
    if isinstance(message, str):
        return BaseMessage.create_message(
            role=MessageRole.USER,
            content=message,
        )
    return message


@macro
def GET_FINAL_MESSAGE(
    response: Optional[Union[BaseMessage, List[BaseMessage]]] = None,
    **kwargs: Any,
) -> BaseMessage:
    r"""Get the final message from llm response.
    If the response is a generator, it will return the last message.
    Otherwise, it will return the response.

    Args:
        response:
            The response to get the final message from.
        kwargs:
            Dict[str, Any]: The local variables of the caller function.

    Returns:
        The final message.

    """
    if response is None:
        response = kwargs.get("__macro_locals__", {}).get("response")
    if not isinstance(response, BaseMessage):
        tmp = None
        for res in response:
            tmp = res
        response = tmp
    return response  # type: ignore[return-value]


@macro
async def ASYNC_GET_FINAL_MESSAGE(
    response: Optional[Union[BaseMessage, List[BaseMessage]]] = None,
    **kwargs: Any,
) -> BaseMessage:
    r"""Get the final message from llm response.
    If the response is a generator, it will return the last message.
    Otherwise, it will return the response.

    Args:
        response:
            The response to get the final message from.
        kwargs:
            Dict[str, Any]: The local variables of the caller function.

    Returns:
        The final message.

    """
    if response is None:
        response = kwargs.get("__macro_locals__", {}).get("response")
    if not isinstance(response, BaseMessage):
        tmp = None
        async for res in response:  # type: ignore[union-attr]
            tmp = res
        response = tmp
    return response  # type: ignore[return-value]


@macro
async def CALL_ASYNC_CALLBACK(
    *args: Any,
    manager: Optional[Union[BaseCallBackManager, AsyncCallBackManager]] = None,
    **kwargs: Any,
) -> None:
    """Asynchronously call a callback manager's methods, handling both sync and
    async managers.

    This macro function automatically handles the callback manager's call
    method, adapting to both synchronous and asynchronous callback managers.

    Args:
        *args:
            Variable positional arguments to pass to the callback.
        manager:
            The callback manager to use. If None, retrieves from the caller's
            context.
        **kwargs:
            Additional keyword arguments to pass to the callback.

    Note:
        - If manager is None, it attempts to get the callback_manager from the
          caller's context.
        - Automatically determines whether to use sync or async call based on
          manager type.
        - Removes internal macro locals from kwargs before calling.

    Example:
        >>> await CALL_ASYNC_CALLBACK("event_name", data=event_data)
    """
    # If no manager provided, get it from the caller's context
    if manager is None:
        manager = kwargs.get("__macro_locals__").get("self").callback_manager  # type: ignore[union-attr]

    # Remove internal macro locals from kwargs to avoid passing to callback
    kwargs.pop("__macro_locals__", None)

    # Handle different types of callback managers
    if isinstance(manager, BaseCallBackManager):
        # For synchronous manager, call directly
        manager.call(*args, **kwargs)
    else:
        # For async manager, await the call
        await manager.call(*args, **kwargs)
