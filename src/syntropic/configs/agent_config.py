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

from pathlib import Path
from typing import Any, Dict, List, Optional, Self, Type, Union

import yaml

from syntropic.configs import BaseConfig
from syntropic.configs.model_config import ModelConfig
from syntropic.configs.tool_config import ToolConfig
from syntropic.prompts.base import BasePrompt
from syntropic.types.enums import AgentType
from syntropic.utils import YAMLLoader


class AgentConfig(BaseConfig):
    name: str
    type: AgentType
    description: Optional[str] = None
    model: Union[List[ModelConfig], ModelConfig]
    prompt: Union[BasePrompt, Dict[str, BasePrompt]]
    tools: Optional[List[ToolConfig]] = None
    # retriever: Optional[str] = None

    @classmethod
    def from_file(cls: Type[Self], path: Path) -> Self:
        try:
            with open(path, "r") as file:
                data = yaml.load(file, YAMLLoader)
        except yaml.YAMLError as e:
            raise ValueError(f"Error loading yaml file {path}: {e}")
        if tools := data.get("tools", None):
            data["tools"] = ToolConfig.parse_tools(tools)

        return cls(**data)

    @classmethod
    def from_dict(cls: Type[Self], data: Dict[str, Any]) -> Self:
        return cls(**data)
