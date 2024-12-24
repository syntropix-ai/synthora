from synthora.workflows import BaseTask
from synthora.workflows import BaseScheduler

def add(x, y):
    return x + y



flow = BaseScheduler()

flow >> BaseTask(add) >> BaseTask(add).s(1) >> BaseTask(add).s(2) >> BaseTask(add).s(3)

print(flow.run(1, 2))

flow = BaseScheduler()

flow | BaseTask(add).s(1) | BaseTask(add).s(2) | BaseTask(add).s(3)

print(flow.run(1))

flow = BaseScheduler()

flow | BaseTask(add).s(1) | BaseTask(add).s(2) | BaseTask(add).si(1, 2)

print(flow.run(1))

flow1 = BaseScheduler(flat_result=True)
flow2 = BaseScheduler()

flow1 | BaseTask(add).si(1, 1) | BaseTask(add).si(1, 2)
flow2 >> BaseTask(add).s(1) >> flow1 >> BaseTask(add) | BaseTask(add).si(1, 2)
print(flow2.run(1))
