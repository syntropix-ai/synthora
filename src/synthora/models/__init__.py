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

from typing import List, Union

from synthora.configs.model_config import ModelConfig
from synthora.types.enums import ModelBackendType
from synthora.types.node import Node

from .base import BaseModelBackend
from .openai_chat import OpenAIChatBackend


BACKEND_MAP = {
    ModelBackendType.OPENAI_CHAT: OpenAIChatBackend,
}


def create_model_from_config(
    config: Union[ModelConfig, List[ModelConfig]], source: Node
) -> Union[BaseModelBackend, List[BaseModelBackend]]:
    """Create a model instance from configuration.

    Args:
        config:
            Model configuration containing backend type, name, model type and
            other configuration parameters.
        source:
            Source node representing the model's origin or context.

    Returns:
        Instantiated model backend based on the configuration.

    Raises:
        KeyError:
            If specified backend type is not found in BACKEND_MAP.
    """
    if isinstance(config, list):
        return [create_model_from_config(c, source) for c in config]
    cls = BACKEND_MAP[config.backend]
    return cls(
        name=config.name,
        source=source,
        model_type=config.model_type,
        config=config.config,
        **(config.backend_config or {}),
    )


__all__ = ["BaseModelBackend", "OpenAIChatBackend", "create_model_from_config"]
