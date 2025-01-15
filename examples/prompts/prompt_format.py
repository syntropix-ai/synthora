from synthora.agents.vanilla_agent import VanillaAgent
from synthora.prompts import BasePrompt


prompt = BasePrompt("Your name is {username}")

# print(prompt.format(username="John Doe"))

agent = VanillaAgent.default(prompt)

print(agent.run("what is your name?", username="John Doe"))