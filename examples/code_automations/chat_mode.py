from synthora.code_automations.agents.agents import create_code_block_generation_chat_agent

agent = create_code_block_generation_chat_agent()

while True:
    user_input = input("Enter your input: ")
    result = agent.run(user_input)
    # print(result) wirte a agent good at math and cal use a tool named 'calculate' to calculate the result(+,-,*,/)
