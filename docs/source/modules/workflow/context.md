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

# Context

In Synthora, **Context** is a powerful mechanism that allows workflows to manage shared state across tasks. By utilizing context, users can implement advanced features such as loops, conditional statements, and dynamic data flow. This document explains how to use context effectively in Synthora workflows, focusing on detailed examples to illustrate the results.

---

## What is Context?

A **Context** is a shared state object that tasks can access and modify during execution. It allows tasks to communicate and store intermediate results, making it a vital component for advanced workflows. Context usage includes:

1. Storing intermediate values.
2. Dynamically controlling task flow (e.g., loops and conditionals).
3. Managing complex data dependencies.

---

## Using Context in Tasks

### Example 1: Storing Intermediate Results
```python
from synthora.workflows.context.base import BaseContext
from synthora.workflows.base_task import BaseTask

def add(ctx: BaseContext, x: int, y: int) -> int:
    with ctx:
        print(ctx.get_state(f"{x + y}"))  # Retrieve a specific state if needed
        if "ans" not in ctx:
            ctx["ans"] = [x + y]  # Store the result in context
        else:
            ctx["ans"] = ctx["ans"] + [x + y]  # Append the result to context
    return x + y
```

#### Explanation of Results:
- On the first execution, `ctx["ans"]` does not exist, so it is initialized with the result of `x + y`.
- On subsequent executions, the new result is appended to `ctx["ans"]`.

---

### Example 2: Using Context for Loop Control

Loops in Synthora workflows can be implemented by controlling the execution flow using context.

```python
def add(ctx: BaseContext) -> int:
    with ctx:
        a = ctx.get("a", 1)
        b = ctx.get("b", 1)
        cnt = ctx.get("cnt", 0)
        print(f"This is {cnt}th time")
        ctx["cnt"] = cnt + 1
        ctx["ans"] = a + b
        ctx["a"] = a + 1
        ctx["b"] = b + 1

        if a + b < 5:  # Continue looping if condition is met
            ctx.set_cursor(-1)  # Repeat the current task
    return int(a + b)
```

#### Workflow Definition
```python
flow = BaseTask(add) >> BaseTask(add).si()
print(flow.run(), flow.get_context()["ans"])
```

#### Execution Steps:
1. **First Iteration**:
   - `a = 1`, `b = 1`, `cnt = 0`.
   - Result is `1 + 1 = 2`, stored in `ctx["ans"]`.
   - `a` and `b` are incremented to `2` each.
   - Loop continues as `a + b = 4` is less than `5`.

2. **Second Iteration**:
   - `a = 2`, `b = 2`, `cnt = 1`.
   - Result is `2 + 2 = 4`, stored in `ctx["ans"]`.
   - `a` and `b` are incremented to `3` and `3`.

3. **Third Iteration**:
   - `a = 3`, `b = 3`, `cnt = 2`.
   - Result is `3 + 3 = 6`, which exceeds `5`.
   - Loop exits.

#### Output:
```plaintext
This is 0th time
This is 1th time
This is 2th time
8 8
```

---

### Example 3: Conditional Logic with Context

Conditional branches in workflows allow tasks to dynamically skip or execute based on context values.

```python
from synthora.types.enums import TaskState

@task(name="skip")
def task1(a: int, b: int) -> int:
    return a + b

@task
def task2(a: int, b: int) -> int:
    print("hello", a, b)
    return a + b

@task
def task0() -> list[int]:
    print("task0")
    return [1, 2]

@task
def bratch(ctx: BaseContext, previous: list[int]) -> int:
    print("bratch", previous)
    with ctx:
        ctx.set_state("skip", TaskState.SKIPPED)
    return previous

bratch.flat_result = True
flow = task0 >> bratch >> (task1 | task2)
```

#### Execution Flow:
1. `task0` runs first and outputs `[1, 2]`.
2. `bratch` receives `[1, 2]` as input, processes it, and sets the state of `task1` to `SKIPPED`.
3. `task2` runs and prints `hello 1 2`.

#### Output:
```plaintext
task0
bratch [1, 2]
hello 1 2
[3, 3]
```

---

## How Results Are Derived

1. **Sequential Tasks**:
   - Results from one task are passed as inputs to the next task unless explicitly overridden.

2. **Context Data Flow**:
   - Tasks read and write to the shared context. This allows for dynamic adjustments, such as repeating tasks or skipping specific ones.

3. **State Management**:
   - Context manages task states (`RUNNING`, `SKIPPED`, etc.), enabling dynamic control over workflow execution.

---

## Additional Functions

This section extends the previous documentation by explaining the additional methods provided in the `BasicContext` class. These methods are crucial for managing the workflow's state, results, and task flow. Even methods that appear to be placeholders (`pass`) will be explained, as they provide hooks for future customization or system interaction.

---

## Additional Methods in `BasicContext`


### Workflow and Cursor Management

#### `@property workflow`
Returns the associated workflow (`BaseScheduler`) for this context.

#### `get_cursor(self) -> int`
Retrieves the current cursor position within the workflow.

#### `set_cursor(self, cursor: int)`
Sets the cursor position, allowing dynamic task flow control.

**Example**:
```python
ctx.set_cursor(-1)  # Set to the first task: task 0
ctx.set_cursor(1)   # Skip to the third task: task 2
```

---

### Task Management

#### `get_task(self, name: str) -> Optional[Union["BaseScheduler", BaseTask]]`
Retrieves a task or sub-scheduler from the workflow by its name.

- Returns the task if found; otherwise, `None`.

**Example**:
```python
task = ctx.get_task("my_task")
if task:
    print(task.state)
```

---

#### `end(self)`
Marks the entire workflow as `COMPLETED`.

**Example**:
```python
ctx.end()
assert ctx.workflow.state == TaskState.COMPLETED
```

---

#### `skip(self, name: str)`
Sets a task's state to `SKIPPED`.

- **`name`**: The name of the task to skip.

**Example**:
```python
ctx.skip("task1")  # Skip the task named "task1"
```

---

### State Management

#### `get_state(self, name: str) -> TaskState`
Retrieves the current state of a specific task.

- **Raises**: `KeyError` if the task is not found.

**Example**:
```python
state = ctx.get_state("task1")
print(f"Task state: {state}")
```

#### `set_state(self, name: str, state: TaskState)`
Sets the state of a specific task.

- **`state`**: Must be a valid `TaskState` enum value.

**Example**:
```python
ctx.set_state("task1", TaskState.RUNNING)
```

---

### Result Management

#### `get_result(self, name: str) -> Any`
Retrieves the result of a specific task.

- **Raises**: `KeyError` if the task is not found.

**Example**:
```python
result = ctx.get_result("task1")
print(f"Task result: {result}")
```

#### `set_result(self, name: str, result: Any)`
Sets the result of a specific task.

**Example**:
```python
ctx.set_result("task1", 42)  # Sets the result of "task1" to 42
```

---

### Lock Management

#### `@property lock`
A placeholder for a lock mechanism that could be used to ensure thread-safe operations in multi-threaded workflows.

#### `acquire(self)`
A placeholder for acquiring the context lock.

#### `release(self)`
A placeholder for releasing the context lock.

These methods are currently implemented as `pass`, meaning they do nothing. They provide a foundation for future development where concurrency control might be needed.

---

### Special Methods

#### `__contains__(self, key: Any) -> bool`
Checks if a key exists in the context.

**Example**:
```python
if "result" in ctx:
    print("Result exists in context.")
```

#### `__getitem__(self, key: Any) -> Any`
Retrieves a value from the context by key.

**Example**:
```python
value = ctx["result"]
```

#### `__setitem__(self, key: Any, value: Any)`
Sets a value in the context by key.

**Example**:
```python
ctx["result"] = 100
```

---

## Summary of Key Methods

| Method                  | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| `get_task(name)`        | Retrieves a task or scheduler by name.                                     |
| `end()`                 | Marks the workflow as completed.                                           |
| `skip(name)`            | Skips the specified task.                                                  |
| `get_state(name)`       | Retrieves the state of a specific task.                                    |
| `set_state(name, state)`| Sets the state of a specific task.                                          |
| `get_result(name)`      | Retrieves the result of a specific task.                                   |
| `set_result(name, result)` | Sets the result of a specific task.                                      |
| `get_cursor()`          | Retrieves the current cursor position in the workflow.                     |
| `set_cursor(cursor)`    | Sets the cursor position, controlling task flow.                           |
| `lock`, `acquire`, `release` | Placeholders for concurrency control mechanisms.                       |

---

This expanded explanation ensures all methods, including placeholders and essential task/state management utilities, are covered in detail.

## Summary

- **Context** enables workflows to manage state, store results, and control task flow dynamically.
- It supports loops, conditionals, and data sharing, making it a versatile tool for advanced workflows.
- By integrating context into tasks, Synthora workflows can handle complex logic and adapt to runtime conditions effectively.

In the next section, we will explore **Schedulers**, which dictate the execution strategy (serial or parallel) for workflows.
