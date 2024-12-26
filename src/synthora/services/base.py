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

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional, Self, Union

from synthora.agents.base import BaseAgent
from synthora.models.base import BaseModelBackend
from synthora.toolkits.base import BaseFunction


class BaseService(ABC):
    def __init__(self) -> None:
        self.service_map: Dict[
            str, Union[Callable[..., Any], BaseAgent, BaseModelBackend]
        ] = {}

    @abstractmethod
    def add(
        self,
        target: Union[BaseFunction, BaseAgent, BaseModelBackend],
        name: Optional[str] = None,
    ) -> Self: ...

    @abstractmethod
    def run(self, *args: Any, **kwargs: Dict[str, Any]) -> Self: ...

    @abstractmethod
    def stop(self) -> Self: ...
