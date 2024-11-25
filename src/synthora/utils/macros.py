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

import inspect
from typing import Any, Dict, List, Optional, Union

from synthora.messages.base import BaseMessage
from synthora.prompts.base import BasePrompt
from synthora.types.enums import MessageRole, NodeType
from synthora.types.node import Node


def macro(func):
    r"""A decorator to create a macro function.
    Macro functions can access the local variables of the caller function.
    """

    def wrapper(*args, **kwargs):
        caller_frame = inspect.currentframe().f_back
        caller_locals = caller_frame.f_locals
        kwargs.update(caller_locals)
        return func(*args, **kwargs)

    return wrapper


@macro
def FORMAT_PROMPT(
    prompt: Optional[Union[BasePrompt, Dict[str, BasePrompt]]] = None,
    **kwargs: Dict[str, Any],
) -> Union[BasePrompt, Dict[str, BasePrompt]]:
    r"""Format the prompt.

    Args:

    - prompt: Optional[Union[BasePrompt, Dict[str, BasePrompt]]]: The prompt to format.
    - kwargs: Dict[str, Any]: The local variables of the caller function.

    Returns:

    - Union[BasePrompt, Dict[str, BasePrompt]]: The formatted prompt.

    """
    if prompt is None:
        prompt = kwargs.get("self").prompt
    params = {**kwargs, **globals()}
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
    **kwargs: Dict[str, Any],
) -> None:
    r"""Update the system message.

    Args:

    - history: Optional[List[BaseMessage]]: The history of the agent.
    - prompt: Optional[BasePrompt]: The prompt of the agent.
    - source: Optional[Node]: The source node of the agent.
    - kwargs: Dict[str, Any]: The local variables of the caller function.
    """
    if not history:
        history = kwargs.get("self").history
    if not prompt:
        prompt = kwargs.get("self").prompt
    if not source:
        source = kwargs.get("self").source
    name = kwargs.get("name", None) or kwargs.get("self").name
    if not history:
        history.append(
            BaseMessage.create_message(
                MessageRole.SYSTEM,
                content=prompt,
                source=Node(name=name, type=NodeType.SYSTEM, ancestor=source),
            )
        )
    else:
        history[0].content = prompt


@macro
def STR_TO_USERMESSAGE(
    message: Optional[Union[str, BaseMessage]] = None,
    **kwargs: Dict[str, Any],
) -> BaseMessage:
    r"""Convert a string to a user message.
    if the input is a string, it will be converted to a user message.
    otherwise, it will be returned as is.

    Args:

    - message: Optional[Union[str, BaseMessage]]: The message to convert.
    - kwargs: Dict[str, Any]: The local variables of the caller function.

    Returns:

    - BaseMessage: The user message.

    """
    if message is None:
        message = kwargs.get("message")
    if isinstance(message, str):
        return BaseMessage.create_message(
            role=MessageRole.USER,
            content=message,
        )
    return message


@macro
def GET_FINAL_MESSAGE(
    response: Optional[Union[BaseMessage, List[BaseMessage]]] = None,
    **kwargs: Dict[str, Any],
) -> BaseMessage:
    r"""Get the final message from llm response.
    If the response is a generator, it will return the last message.
    Otherwise, it will return the response.

    Args:

    - response: Optional[Union[BaseMessage, List[BaseMessage]]]: The response to get the final message from.
    - kwargs: Dict[str, Any]: The local variables of the caller function.

    Returns:

    - BaseMessage: The final message.

    """
    if response is None:
        response = kwargs.get("response")
    if not isinstance(response, BaseMessage):
        tmp = None
        for res in response:
            tmp = res
        response = tmp
    return response
