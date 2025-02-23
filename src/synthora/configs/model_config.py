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

from pathlib import Path
from typing import Any, Dict, Optional, Type


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

import yaml

from synthora.configs.base import BaseConfig
from synthora.types.enums import ModelBackendType
from synthora.utils import YAMLLoader


class ModelConfig(BaseConfig):
    """Configuration class for AI models

    Attributes:
        model_type:
            Type identifier of the model (e.g., 'gpt-4', 'claude-3').
        name:
            Optional custom name for the model instance.
        backend:
            Backend system type, defaults to OPENAI_CHAT.
        config:
            Optional model-specific configuration parameters.
        backend_config:
            Optional backend-specific configuration.
    """

    model_type: str
    name: Optional[str] = None
    backend: ModelBackendType = ModelBackendType.OPENAI_CHAT
    config: Optional[Dict[str, Any]] = None
    backend_config: Optional[Dict[str, Any]] = None

    @classmethod
    def from_file(cls: Type[Self], path: Path) -> Self:
        """Load model configuration from a YAML file

        Args:
            path:
                Path to the YAML configuration file.

        Returns:
            Instance of ModelConfig.

        Raises:
            ValueError:
                If YAML file cannot be loaded properly.
        """
        try:
            with open(path, "r") as file:
                data = yaml.load(file, YAMLLoader)
        except yaml.YAMLError as e:
            raise ValueError(f"Error loading yaml file {path}: {e}")
        return cls(**data)

    @classmethod
    def from_dict(cls: Type[Self], data: Dict[str, Any]) -> Self:
        """Create model configuration from a dictionary

        Args:
            data:
                Dictionary containing model configuration.

        Returns:
            Instance of ModelConfig.
        """
        return cls(**data)
