from pathlib import Path
from typing import Any, Dict, List, Optional, Self, Type, Union
from syntropic.configs import BaseConfig
from syntropic.models.base import BaseModelBackend
import yaml
from syntropic.utils import YAMLLoader
from syntropic.types.enums import ModelBackendType

class ToolConfig(BaseConfig):
    
    target: Optional[str] = None
    trace: Optional[bool] = True
    args: Optional[Dict[str, Any]] = None

    @classmethod
    def from_file(cls: Type[Self], path: Path) -> Self:
        try:
            with open(path, "r") as file:
                data = yaml.load(file, YAMLLoader)
        except yaml.YAMLError as e:
            raise ValueError(f"Error loading yaml file {path}: {e}")
        return cls(**data)

    @classmethod
    def from_dict(cls: Type[Self], data: Dict[str, Any]) -> Self:
        return cls(**data)
    
    @staticmethod
    def parse_tools(plugins: List[Union[str, Dict[str, Any]]]) -> List["ToolConfig"]:
        parsed_plugins = []
        for plugin in plugins:
            if isinstance(plugin, str):
                parsed_plugins.append(ToolConfig(target=plugin, args={}))
            else:
                parsed_plugins.append(ToolConfig(**plugin))
        return parsed_plugins
