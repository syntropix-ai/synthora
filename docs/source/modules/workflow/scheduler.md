<!-- LICENSE HEADER MANAGED BY add-license-header

Copyright 2024-2025 Syntropix

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Scheduler

The **Scheduler** is a core component in Synthora's workflow system, responsible for managing the execution of tasks. It determines the order and concurrency of task execution, enabling workflows to process tasks serially, in parallel, or in a combination of both.

---

## Scheduler Overview

A **Scheduler** defines how tasks are executed in a workflow. Synthora provides different schedulers to handle task execution strategies:

1. **BaseScheduler**: Executes tasks serially.
2. **ThreadPoolScheduler**: Executes tasks concurrently using threads.
3. **ProcessPoolScheduler**: Executes tasks concurrently using separate processes.

Schedulers also support advanced configurations, such as task grouping, predefining inputs, and integrating serial and parallel workflows.

---

## Creating a Scheduler

### BaseScheduler: Serial Execution

Tasks are executed one after another. Each task’s output is passed as input to the next task in sequence.

#### Example
```python
from synthora.workflows.scheduler import BaseScheduler
from synthora.workflows.base_task import BaseTask

# Define a task function
def add(x: int, y: int) -> int:
    return x + y

# Create a scheduler
scheduler = BaseScheduler()

# Add tasks
scheduler.add_task(BaseTask(add, name="task1").s(1))  # Predefine x = 1
scheduler.add_task(BaseTask(add, name="task2").s(2))  # Predefine x = 2

# Run the workflow
result = scheduler.run(1)  # y = 1 is passed as input
print(result)  # Output: 4
```

**Explanation**:
1. The first task (`task1`) receives `x=1` and `y=1`. It returns `1 + 1 = 2`.
2. The second task (`task2`) receives `x=2` (predefined) and `y=2` (output from the previous task). It returns `2 + 2 = 4`.

---

### ThreadPoolScheduler: Parallel Execution

Tasks are executed concurrently, sharing the same input parameters.

#### Example
```python
from synthora.workflows.scheduler import ThreadPoolScheduler

# Define a task
def multiply(x: int, y: int) -> int:
    return x * y

# Create a scheduler
scheduler = ThreadPoolScheduler()

# Add tasks
scheduler.add_task_group(
    BaseTask(multiply).s(2), # Predefine x = 2
    BaseTask(multiply).s(3), # Predefine x = 3
    BaseTask(multiply).s(4), # Predefine x = 4
    )

# Run the workflow
result = scheduler.run(5)  # y = 5 is passed as input
print(result)  # Output: [10, 15, 20]
```

**Explanation**:
1. Each task (`x=2`, `x=3`, `x=4`) runs in parallel with the same input `y=5`.
2. Results:
   - Task 1: `2 * 5 = 10`
   - Task 2: `3 * 5 = 15`
   - Task 3: `4 * 5 = 20`
3. The scheduler collects and returns the results as a list: `[10, 15, 20]`.

---

### Combining Serial and Parallel Execution

Synthora allows serial and parallel workflows to be combined for more complex task orchestration.

#### Example
```python
from synthora.workflows.base_task import BaseTask

# Define a task
def add(x: int, y: int) -> int:
    return x + y

# Create a combined workflow
flow = (
    BaseTask(add).s(1)         # Parallel task
    | BaseTask(add).s(2)       # Parallel task
) >> BaseTask(add)             # Serial task

# Run the workflow
result = flow.run(1)  # y = 1 is passed as input
print(result)  # Output: 5
```

**Explanation**:
1. Two parallel tasks (`add.s(1)` and `add.s(2)`) execute with `x=1` and `x=2` respectively:
   - Parallel Task 1: `1 + 1 = 2`
   - Parallel Task 2: `1 + 2 = 3`
2. The results `[2, 3]` are passed to the final serial task (`add`). The task adds these results: `2 + 3 = 5`.

---

### ProcessPoolScheduler: High-Performance Parallel Execution

The `ProcessPoolScheduler` is similar to the `ThreadPoolScheduler` but uses separate processes, making it suitable for CPU-intensive tasks.

#### Example
```python
from synthora.workflows.scheduler.process_pool import ProcessPoolScheduler

# Define a task
def square(x: int) -> int:
    return x ** 2

# Create a process pool scheduler
scheduler = ProcessPoolScheduler()

# Add tasks
scheduler.add_task_group(
    BaseTask(square).s(2), BaseTask(square).s(3), BaseTask(square).s(4)
    )

# Run the workflow
result = scheduler.run()  # No additional inputs required
print(result)  # Output: [4, 9, 16]
```

**Explanation**:
1. Each task computes the square of its predefined parameter:
   - Task 1: `2 ** 2 = 4`
   - Task 2: `3 ** 2 = 9`
   - Task 3: `4 ** 2 = 16`
2. The scheduler collects and returns the results as a list: `[4, 9, 16]`.

---

### Serial Workflows Using Operators

Synthora supports Python operators to simplify serial task chaining.

#### Example
```python
flow = BaseTask(add).s(1) >> BaseTask(add).s(2) >> BaseTask(add).s(3)
result = flow.run(1)  # y = 1 is passed as input
print(result)  # Output: 7
```

**Explanation**:
1. Task 1: `1 + 1 = 2`
2. Task 2: `2 + 2 = 4`
3. Task 3: `4 + 3 = 7`

---

### Parallel Workflows Using Operators

Parallel workflows can also be defined using the `|` operator.

#### Example
```python
flow = BaseTask(add).s(1) | BaseTask(add).s(2) | BaseTask(add).s(3)
result = flow.run(1)  # y = 1 is passed as input
print(result)  # Output: [2, 3, 4]
```

**Explanation**:
1. Each task (`x=1`, `x=2`, `x=3`) runs in parallel with the same input `y=1`.
2. Results:
   - Task 1: `1 + 1 = 2`
   - Task 2: `2 + 1 = 3`
   - Task 3: `3 + 1 = 4`

---

### Nested Workflows

Workflows can be nested for added complexity.

#### Example
```python
flow = (
    (BaseTask(add).s(1) | BaseTask(add).s(2)) >> BaseTask(add)
)
result = flow.run(1)
print(result)  # Output: 5
```

**Explanation**:
1. Two parallel tasks execute first:
   - Parallel Task 1: `1 + 1 = 2`
   - Parallel Task 2: `1 + 2 = 3`
2. Their results `[2, 3]` are passed to the final task:
   - Final Task: `2 + 3 = 5`

---

## Summary

Schedulers in Synthora provide powerful tools to manage task execution. By combining **serial**, **parallel**, and **nested** workflows, users can build complex, high-performance workflows tailored to their needs. Detailed explanations of results help ensure transparency in how workflows are structured and executed.
