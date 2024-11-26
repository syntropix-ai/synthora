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

from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar


T = TypeVar("T")
E = TypeVar("E", bound=Exception)


class Result(Generic[T, E]):
    """Base class for Result"""

    @property
    def is_ok(self) -> bool:
        raise NotImplementedError

    @property
    def is_err(self) -> bool:
        raise NotImplementedError


@dataclass
class Ok(Result[T, E]):
    value: T

    @property
    def is_ok(self) -> bool:
        return True

    @property
    def is_err(self) -> bool:
        return False


@dataclass
class Err(Result[T, E]):
    error: E
    value: T

    @property
    def is_ok(self) -> bool:
        return False

    @property
    def is_err(self) -> bool:
        return True


class AgentType(str, Enum):
    VANILLA = "vanilla"
    REACT = "react"
    REWOO = "rewoo"
    COT = "cot"
    TOT = "tot"
    REFLECTION = "reflection"


class ModelBackendType(str, Enum):
    OPENAI_CHAT = "openai_chat"


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL_RESPONSE = "tool_response"


class NodeType(str, Enum):
    AGENT = "agent"
    MODEL = "model"
    TOOL = "tool"
    USER = "user"
    SYSTEM = "system"


class CallBackEvent(str, Enum):
    LLM_START = "on_llm_start"
    LLM_END = "on_llm_end"
    LLM_ERROR = "on_llm_error"
    LLM_CHUNK = "on_llm_chunk"
    TOOL_START = "on_tool_start"
    TOOL_END = "on_tool_end"
    TOOL_ERROR = "on_tool_error"
    AGENT_START = "on_agent_start"
    AGENT_END = "on_agent_end"
    AGENT_ERROR = "on_agent_error"
