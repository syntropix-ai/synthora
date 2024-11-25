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

from synthora.configs.model_config import ModelConfig
from synthora.types.enums import ModelBackendType

from .base import BaseModelBackend
from .openai_chat import OpenAIChatBackend


BACKEND_MAP = {
    ModelBackendType.OPENAI_CHAT: OpenAIChatBackend,
}


def create_model_from_config(config: ModelConfig) -> BaseModelBackend:
    cls = BACKEND_MAP[config.backend]
    return cls(
        name=config.name,
        model_type=config.model_type,
        config=config.config,
        **(config.backend_config or {}),
    )


__all__ = ["BaseModelBackend", "OpenAIChatBackend", "create_model_from_config"]
