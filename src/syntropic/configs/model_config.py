from pathlib import Path
from typing import Any, Dict, Optional, Self, Type
from syntropic.configs import BaseConfig
from syntropic.models.base import BaseModelBackend
import yaml
from syntropic.utils import YAMLLoader
from syntropic.types.enums import ModelBackendType

class ModelConfig(BaseConfig):
    name: str
    backend: ModelBackendType = ModelBackendType.OPENAI
    config: Optional[Dict[str, Any]] = None
    backend_config: Optional[Dict[str, Any]] = None

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
