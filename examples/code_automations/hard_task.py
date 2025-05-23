from synthora.code_automations.blocks import *
from synthora.code_automations.graph import AutomationGraph


block00 = InputBlock("input-pdf", "read the pdf file from input.pdf")
block01 = InputBlock("input-company", "read a company list from input.json")

block10 = CodeBlock("vectorize", "vectorize the pdf file using llamaindex's bm25", extra_dependencies=[block00])

block20 = LoopBlock("loop-company", "for every company in the company list, search name in the vectorized pdf file using bm25. collect the results to a list.", extra_dependencies=[block01, block10])


block30 = CodeBlock("answer", "save the results to a json file", extra_dependencies=[block20])

block40 = CodeBlock("agent", "define an agent good at answering questions", extra_dependencies=[block10])

block50 = LoopBlock("answer", "while user input != 'q', ask agent and print the answer", extra_dependencies=[block40])



graph = AutomationGraph("A math agent", [block00, block01, block10, block20, block30, block40, block50])

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



