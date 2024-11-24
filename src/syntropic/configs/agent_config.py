from pathlib import Path
from typing import Any, Dict, List, Optional, Self, Type, Union
from syntropic.agents.base import BaseAgent
from syntropic.configs import BaseConfig
from syntropic.configs.model_config import ModelConfig
from syntropic.configs.tool_config import ToolConfig
from syntropic.models.base import BaseModelBackend
import yaml
from syntropic.prompts.base import BasePrompt
from syntropic.toolkits.base import BaseFunction
from syntropic.utils import YAMLLoader
from syntropic.types.enums import AgentType, ModelBackendType


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
