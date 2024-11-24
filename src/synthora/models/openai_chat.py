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

import os
from typing import Any, Dict, Optional

from synthora.models import BaseModelBackend
from openai import OpenAI


class OpenAIChatBackend(BaseModelBackend):
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.kwargs = kwargs
        self.config = config or {}
        self.kwargs["api_key"] = self.api_key
        self.kwargs["base_url"] = self.base_url

        self.client = OpenAI(**self.kwargs)

        super().__init__()

    def run(self, **kwargs: Dict[str, Any]) -> Any:
        return self.client.chat.completions.create(**kwargs)

    async def async_run(self, **kwargs: Dict[str, Any]) -> Any:
        return self.client.chat.conversations.create(**kwargs)
