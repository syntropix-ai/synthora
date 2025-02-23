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

# Reasoning and Acting Agent (ReAct) Agent

The **ReAct Agent** (Reasoning and Acting Agent) is an advanced implementation in the Synthora framework. It combines reasoning capabilities with the ability to dynamically execute actions using tools. This design enables the agent to interact with tools in real-time while reasoning through problems step by step.

---

## Overview

### Purpose
The ReAct Agent enables reasoning about actions and executing them iteratively.

### Key Features
1. **Reasoning and Acting**:
   - Combines reasoning steps with tool invocations, creating a seamless decision-making process.
2. **Asynchronous and Synchronous Execution**:
   - Supports both synchronous and asynchronous processing, making it versatile for various applications.

---

## Implementation

### Code Example

#### Creating and Using a ReAct Agent

```python
from synthora.agents.react import ReactAgent

# Create a ReAct Agent with the ReAct prompt
agent = ReactAgent.default()

# Process a query
response = agent.run("What is 15% of 120?")
print(response.unwrap())
```

---

### Key Methods

#### `step()`
Processes a single input message and determines the next action, which may include invoking tools.

**Arguments**:
- `message` (str or BaseMessage): Input message to process.

**Returns**:
- A `Result` object containing either the agent's response or an exception.

**Example**:
```python
response = agent.step("What is 12 times 8?")
print(response.unwrap())  # Outputs intermediate reasoning and the final result.
```

---

#### `run()`
Executes the full reasoning and acting loop, processing input messages until a final response is generated or the `finish` tool is called.

**Arguments**:
- `message` (str or BaseMessage): The input message to process.

**Returns**:
- A `Result` object with the final response or an exception.

**Example**:
```python
response = agent.run("How do you bake a cake?")
print(response.unwrap())  # Outputs step-by-step instructions for baking a cake.
```

---

#### `add_tool()` and `remove_tool()`
- Dynamically add or remove tools from the agent's toolset.
- Tools include both pre-defined functions and custom implementations.

**Example**:
```python
# Add a tool
agent.add_tool(my_custom_tool)

# Remove a tool
agent.remove_tool(my_custom_tool)
```

---

### Asynchronous Methods

Synthora's ReAct Agent supports asynchronous operations, enabling efficient processing for tasks that require real-time interactions.

- **`async_step()`**: Processes a single input asynchronously.
- **`async_run()`**: Executes the reasoning and acting loop asynchronously.

---

## Summary

The **ReAct Agent** is a powerful tool for combining reasoning and dynamic action execution. By leveraging tools like `finish` and supporting step-by-step reasoning, it excels in tasks requiring intermediate steps and decision-making. Its ability to handle both synchronous and asynchronous workflows makes it ideal for diverse applications, from problem-solving to task automation.
