from synthora.code_automations.blocks import *
from synthora.code_automations.graph import AutomationGraph

block0 = InputBlock("block0", "Read input from inp.txt")
block1 = CodeBlock("block1", "Print the input")
block3 = CodeBlock("block2", "Convert input to int", extra_dependencies=[block0])
block4 = ConditionBlock("block3", "Check if the input is even, if so, print 'even', run block5, otherwise print 'odd', run block6")
block5 = LoopBlock("block5", "Loop through the input, and print the input")
block6 = CodeBlock("block6", "Print 'even'")
block7 = CodeBlock("block7", "return 0", extra_dependencies=[block5, block6])

block0 >> block1 >> block3 >> block4 >> block5
block4 >> block6
block4 >> block7


graph = AutomationGraph("A test code", [block0, block1, block3, block4, block5, block6, block7])

print(graph)

result = graph.run()

print(result)

# print(block0.code)
# print(block1.code)
# print(block3.code)
# print(block4.code)
# print(block5.code)
# print(block6.code)
# print(block7.code)



