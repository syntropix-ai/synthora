from synthora.agents.tot_agent import ToTAgent

agent = ToTAgent.default()

print(agent.run("1 * -1 + 177 - 16 = ?"))