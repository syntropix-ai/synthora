from synthora.agents import BaseAgent, VanillaAgent
from synthora.configs import AgentConfig
from synthora.messages import BaseMessage
from synthora.types.enums import MessageRole, NodeType
from synthora.types.node import Node


config = AgentConfig.from_file("examples/agents/configs/vanilla_agent.yaml")
print(config)

agent = VanillaAgent.from_config(config)


print(agent.run("Search Trump on Wikipedia"))
