from synthora.code_automations.blocks import *
from synthora.code_automations.graph import AutomationGraph


block0 = CodeBlock("agent", "define an agent good at math(can use calculator: +,-,*,/)")
block1 = LoopBlock("loop", "while True")
block2 = CodeBlock("input", "Let's user to input a query")

block3 = CodeBlock("check input", "if input is 'q', break the loop", extra_dependencies=[block2])
block4 = CodeBlock("answer", "ask agent and print the answer", extra_dependencies=[block2, block0])


block0 >> block1 >> block2 >> block3 >> block4


graph = AutomationGraph("A math agent", [block0, block1, block2, block3, block4])

result = graph.run()

print(result)

with open("test.py", "w") as f:
    f.write(result)

# print(block0.code)
# print(block1.code)
# print(block3.code)
# print(block4.code)
# print(block5.code)
# print(block6.code)
# print(block7.code)



