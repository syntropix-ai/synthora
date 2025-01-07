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

from typing import List, Optional, Union

from synthora.agents.base import BaseAgent
from synthora.agents.vanilla_agent import VanillaAgent
from synthora.callbacks.base_handler import AsyncCallBackHandler, BaseCallBackHandler
from synthora.configs.agent_config import AgentConfig
from synthora.configs.model_config import ModelConfig
from synthora.models import create_model_from_config
from synthora.prompts.base import BasePrompt
from synthora.prompts.buildin import FewShotReactPrompt
from synthora.toolkits.base import BaseFunction
from synthora.types.enums import AgentType, NodeType
from synthora.types.node import Node


class ReactAgent(VanillaAgent):
    """A ReAct (Reasoning and Acting) agent implementation.

    This agent follows the ReAct pattern of reasoning about actions and executing them.
    It can use tools to accomplish tasks and maintains a conversation history.

    Args:
        config (AgentConfig): Configuration for the agent
        source (Node): Source node for the agent
        model (BaseModelBackend): The underlying model for reasoning
        prompt (BasePrompt): The prompt template for the agent
        tools (List[Union[BaseAgent, BaseFunction]], optional): List of available tools. Defaults to [].
    """

    @staticmethod
    def default(
        prompt: Optional[str] = None,
        name: str = "React",
        model_type: str = "gpt-4o",
        tools: Optional[List[Union["BaseAgent", BaseFunction]]] = None,
        handlers: Optional[
            List[Union[BaseCallBackHandler, AsyncCallBackHandler]]
        ] = None,
    ) -> "ReactAgent":
        r"""Create a default ReAct agent with the specified prompt and tools.

        Args:
            prompt (str): The initial prompt for the agent
            name (str, optional): The name of the agent. Defaults to "React".
            model_type (str, optional): The model type to use. Defaults to "gpt-4o".
            tools (List[Union["BaseAgent", BaseFunction]], optional): List of available tools. Defaults to [].
            handlers (List[Union[BaseCallBackHandler, AsyncCallBackHandler]], optional): List of callback handlers. Defaults to [].

        Returns:
            ReactAgent: The created ReAct agent
        """
        prompt = prompt or FewShotReactPrompt
        tools = tools or []
        handlers = handlers or []
        config = AgentConfig(
            name=name,
            type=AgentType.REACT,
            model=ModelConfig(model_type=model_type, name=model_type),
            prompt=BasePrompt(prompt),
            tools=tools,
        )
        node = Node(name=name, type=NodeType.AGENT)
        model = create_model_from_config(config.model, node)
        agent = ReactAgent(
            config,
            Node(name=name, type=NodeType.AGENT),
            model,
            config.prompt,  # type: ignore[arg-type]
            config.tools,  # type: ignore[arg-type]
        )
        if handlers:
            for handler in handlers:
                agent.add_handler(handler)
        return agent
