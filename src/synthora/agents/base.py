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

import importlib
import inspect
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Self, Type, Union

from synthora.callbacks import get_callback_manager
from synthora.callbacks.base_handler import AsyncCallBackHandler, BaseCallBackHandler
from synthora.configs.agent_config import AgentConfig
from synthora.messages.base import BaseMessage
from synthora.models import create_model_from_config
from synthora.models.base import BaseModelBackend
from synthora.prompts.base import BasePrompt
from synthora.toolkits.base import BaseFunction, BaseToolkit
from synthora.types.enums import NodeType, Result
from synthora.types.node import Node


class BaseAgent(ABC):
    def __init__(
        self,
        config: AgentConfig,
        source: Node,
        model: Union[BaseModelBackend, List[BaseModelBackend]],
        prompt: Union[BasePrompt, Dict[str, BasePrompt]],
        tools: List[Union["BaseAgent", BaseFunction]] = [],
        handlers: List[Union[BaseCallBackHandler, AsyncCallBackHandler]] = [],
    ) -> None:
        self.config = config
        self.source = source
        self.name = self.config.name
        self.type = self.config.type
        self.description = self.config.description
        self.model = model
        self.prompt = prompt
        self.tools = tools
        self.history: List[BaseMessage] = []
        self.callback_manager = get_callback_manager(handlers)

    @property
    def schema(self) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def run(
        self, message: str, *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]: ...

    @abstractmethod
    async def async_run(
        self, message: str, *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]: ...

    @abstractmethod
    def step(
        self, message: str, *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]: ...

    @abstractmethod
    async def async_step(
        self, message: str, *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]: ...

    @classmethod
    def from_config(cls: Type[Self], config: AgentConfig) -> Self:
        _model = config.model if isinstance(config.model, list) else [config.model]
        model = [create_model_from_config(m) for m in _model]
        tools = []
        source = Node(name=config.name, type=NodeType.AGENT)
        if isinstance(config.prompt, dict):
            prompt = {}
            for key, value in config.prompt.items():
                prompt[key] = BasePrompt(value)
        else:
            prompt = BasePrompt(config.prompt)

        for tool in config.tools or []:
            try:
                if "." not in tool.target:
                    module = importlib.import_module(tool.target)
                else:
                    module = importlib.import_module(tool.target.rsplit(".", 1)[0])
                    module = getattr(module, tool.target.rsplit(".", 1)[1])

                if not inspect.isclass(module):
                    raise ValueError(
                        f"Expected class in module {tool.target}, got {type(module)}"
                    )
                if issubclass(module, BaseToolkit):
                    instance = module(**tool.args)
                    tools.extend(instance.sync_tools)
                    tools.extend(instance.async_tools)
                elif issubclass(module, BaseAgent):
                    agent_config = AgentConfig.from_dict(tool.args or {})
                    instance = module.from_config(agent_config)
                    tools.append(instance)
                elif issubclass(module, BaseFunction):
                    instance = module(**tool.args)
                    tools.append(instance)
            except ImportError:
                raise ImportError(f"Could not import {tool.target}")
            except Exception as e:
                raise ValueError(
                    f"Error loading toolkit {tool.target} with args {tool.args}: {e}"
                )
        for tool in tools:
            if tool.source:
                tool.source.ancestor = source
        return cls(
            config=config, model=model, prompt=prompt, tools=tools, source=source
        )

    def get_tool(self, name: str) -> Union[BaseFunction, "BaseAgent"]:
        for tool in self.tools:
            if tool.name == name:
                return tool
        raise ValueError(f"Tool {name} not found in agent {self.name}")
