from syntropic.configs import AgentConfig

config = AgentConfig.load("examples/configs/configs/basic_agent.yaml")
print(config.prompt.format(x="1"))
print(config)
