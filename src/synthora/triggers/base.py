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

from abc import ABC, abstractmethod
from typing import Optional, Union


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from synthora.agents.base import BaseAgent
from synthora.toolkits.base import BaseFunction


class BaseTrigger(ABC):
    def __init__(self, args_name: str) -> None:
        self.args_name = args_name

    @abstractmethod
    def add(self, obj: Union[BaseFunction, BaseAgent]) -> Self: ...

    @abstractmethod
    def start(self) -> Self: ...

    @abstractmethod
    def stop(self, wait: bool = True) -> Self: ...

    def wrap_agent(
        self,
        agent: BaseAgent,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> BaseAgent:
        if name:
            agent.schema["function"]["name"] = name  # type: ignore
        if description:
            agent.schema["function"]["description"] = description  # type: ignore
        else:
            agent.schema["function"][  # type: ignore[index]
                "description"
            ] = r"""
            Call the function will trigger yourself at the specified time.
            Used when you want to do something at a specific time.
            You should provide the time in the format of 'YYYY-MM-DD HH:MM:SS'
            and a message reminding you of the task.
            """
        self.add(agent)
        return agent
