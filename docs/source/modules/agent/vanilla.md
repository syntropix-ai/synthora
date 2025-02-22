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

# Vanilla Agent

The **VanillaAgent** is the most basic implementation of an agent in the Synthora framework. It provides a simple, extensible interface for sequential message processing, tool invocation, and maintaining conversation history.

---

## Overview

### Purpose
- The VanillaAgent serves as a foundation for building more advanced agents by providing essential functionality.
- It processes messages, invokes tools, and maintains a structured conversation history.

### Core Features
1. **Message Processing**: Handles messages sequentially, updating system prompts and appending responses to conversation history.
2. **Tool Invocation**: Supports calling tools (e.g., BaseFunction or other agents) dynamically during message processing.
3. **History Maintenance**: Keeps track of the conversation for context-aware responses.

---

## Key Methods

### Initialization
The agent is initialized with configurations, a prompt template, a model, and an optional list of tools.

#### `VanillaAgent.default()`
Creates a default VanillaAgent instance with common configurations.

**Arguments**:
- `prompt` (str): The prompt template for the agent (default is `VanillaPrompt`).
- `name` (str): The agent's name (default is `"Vanilla"`).
- `model_type` (str): The model type to use (default is `"gpt-4o"`).
- `tools` (Optional[List]): Tools available to the agent.
- `handlers` (Optional[List]): Callback handlers for the agent.

**Example**:
```python
agent = VanillaAgent.default(
    prompt="What can I help you with?",
    name="SimpleAgent",
    model_type="gpt-3.5",
    tools=[some_tool]
)
```

---

### Core Methods

#### `step()`
Processes a single input message and generates a response.

**Arguments**:
- `message` (str or BaseMessage): The input message to process.

**Returns**:
- A `Result` object containing either the model's response or an exception.

**Example**:
```python
response = agent.step("Hello, how are you?")
print(response.unwrap())  # Outputs the agent's response.
```

---

#### `run()`
Executes the complete message processing loop, handling tool calls if required. Continues until a final response without tool calls is reached or an error occurs.

**Arguments**:
- `message` (str or BaseMessage): The input message to process.

**Returns**:
- A `Result` object with the final response or an exception.

**Example**:
```python
response = agent.run("What is the capital of France?")
print(response.unwrap())  # Outputs "The capital of France is Paris."
```

---

#### `add_tool()`
Adds a tool to the agent's toolset dynamically.

**Arguments**:
- `tool` (BaseFunction or BaseAgent): The tool to add.

**Returns**:
- The agent instance (for chaining).

**Example**:
```python
agent.add_tool(new_tool)
```

---

#### `remove_tool()`
Removes a tool from the agent's toolset.

**Arguments**:
- `tool` (BaseFunction or BaseAgent): The tool to remove.

**Returns**:
- The agent instance (for chaining).

**Example**:
```python
agent.remove_tool(existing_tool)
```

---

#### `reset()`
Clears the agent's conversation history.

**Returns**:
- The agent instance (for chaining).

**Example**:
```python
agent.reset()
```

---

### Asynchronous Methods

Synthora's VanillaAgent also includes placeholders for asynchronous processing:

- **`async_step()`**: Processes a single message asynchronously.
- **`async_run()`**: Executes the entire message processing loop asynchronously.

---

## Use Cases

- **Basic Chat Applications**: Ideal for creating simple conversational agents with minimal setup.
- **Testing and Debugging**: Provides a clear structure for testing prompt designs and tool integrations.
- **Foundational Customization**: Serves as a base class for building more complex agents like Cot, ToT, or ReAct agents.

---

## Summary

The **VanillaAgent** provides a straightforward and flexible foundation for creating agents in Synthora. Its modular design allows seamless integration of tools and supports both synchronous and asynchronous workflows. As the simplest agent type, it is perfect for rapid prototyping and serves as the building block for more advanced agents.
