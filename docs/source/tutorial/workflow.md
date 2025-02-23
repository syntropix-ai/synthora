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

# Build Powerful Workflows with Synthora! 🚀

Unlock the potential of dynamic workflows with Synthora! This guide will walk you through setting up workflows using **BaseTask** and **BaseContext** to manage complex logic with ease.

---

## What Are Workflows? 🤔

Workflows in Synthora let you chain tasks together and handle state seamlessly:
- Reuse common logic
- Manage task dependencies
- Process tasks sequentially or in parallel

---

## Create a Simple Workflow 🛠️

Here’s how to create a straightforward task flow using `BaseTask`:

```python
from synthora.workflows import BaseTask
from synthora.workflows.context.base import BaseContext


def add(ctx: BaseContext, x: int, y: int) -> int:
    if "ans" not in ctx:
        ctx["ans"] = [x + y]
    else:
        ctx["ans"].append(x + y)
    print(ctx.get_state(f"{x + y}"))
    return x + y


flow = (
    BaseTask(add, "3")
    >> BaseTask(add, "4").s(1)
    >> BaseTask(add, "6").s(2)
    >> BaseTask(add, "9").s(3)
)

print(flow.run(1, 2), flow.get_context()["ans"])
```

### Key Features:
- **BaseTask**: Encapsulates individual functions into reusable tasks.
- **Flow Operators**: Use `>>` for sequential execution.
- **Context Tracking**: Store intermediate results using `BaseContext`.

---

## Handling Task State 💡

Track and manage task states (e.g., `SKIPPED`, `COMPLETED`) for better control over execution:

```python
from synthora.workflows.context.base import BaseContext, TaskState


def add(ctx: BaseContext, x: int, y: int) -> int:
    with ctx:
        ctx.set_state("skip", TaskState.SKIPPED)
        if "ans" not in ctx:
            ctx["ans"] = [x + y]
        else:
            ctx["ans"] = ctx["ans"] + [x + y]
    return x + y


def skip(ctx: BaseContext, x: int, y: int) -> int:
    with ctx:
        ctx.set_state("skip_task", TaskState.COMPLETED)
        if "ans" not in ctx:
            ctx["ans"] = [x + y]
        else:
            ctx["ans"] = ctx["ans"] + [x + y]
    return x + y
```

### Use with a Scheduler:
```python
from synthora.workflows import ProcessPoolScheduler

flow = ProcessPoolScheduler()
flow | BaseTask(add, "2").s(1) | BaseTask(add, "3").s(2) | BaseTask(add, "4").s(3)

flow >> BaseTask(add, "skip").si(1, 2)

print(flow.run(1), flow.get_context()["ans"])
```

---

## Parallel Task Execution ⚡

Execute multiple tasks in parallel using `|` (OR operator):

```python
from synthora.workflows import BaseTask


def add(x: int, y: int) -> int:
    return x + y


# Parallel Execution
flow = BaseTask(add).s(1) | BaseTask(add).s(2) | BaseTask(add).s(3)

print(flow.run(1))
```

---

## Nested and Complex Flows 🧩

Combine sequential and parallel execution for complex workflows:

```python
flow1 = (BaseTask(add).si(1, 1) | BaseTask(add).si(1, 2)).set_flat_result(True)
flow2 = BaseTask(add).s(1) >> flow1 >> (BaseTask(add) | BaseTask(add).si(1, 2))
print(flow2.run(1))

print(flow2)
```

---

## Workflow Tips & Tricks 🌟

1. **Set Results Flat**:
   Flatten nested results for easier processing:
   ```python
   flow1 = (BaseTask(add).si(1, 1) | BaseTask(add).si(1, 2)).set_flat_result(True)
   ```

2. **Chain Multiple Tasks**:
   Use `>>` for chaining tasks sequentially or `|` for parallel execution:
   ```python
   flow = BaseTask(add) >> BaseTask(add).s(1) | BaseTask(add).s(2)
   ```

3. **Custom Context Management**:
   Leverage `BaseContext` to maintain shared states across tasks.

---

## Ready to Take It Further? 🌈

Master Synthora workflows by combining tasks, managing states, and optimizing performance. For more advanced examples and documentation, visit the [Synthora Workflows Docs](https://synthora.readthedocs.io/)!
