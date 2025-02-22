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

# Callback

Understand what's happening inside your agent with Synthora's callback system. Callbacks provide a powerful way to log and track events throughout your agent's workflow.

---

## What Are Callbacks?

Callbacks act as event listeners, providing updates on various stages of your agent's operations. They notify you when:
- The agent starts processing.
- A tool is utilized.
- Decisions are made.
- An error occurs.

---

## Adding Callbacks to Your Agent

Implementing callbacks in your agent is simple. Below is an example of how to add logging with console output:

```python
from synthora.agents import ReactAgent
from synthora.configs import AgentConfig
from synthora.callbacks import RichOutputHandler

# Create your agent
config = AgentConfig.from_file("examples/agents/configs/react_agent.yaml")
agent = ReactAgent.from_config(config)

# Add console output in two lines
handler = RichOutputHandler()
agent.add_handler(handler)

# Run the agent and observe the output
agent.run("Search OpenAI on Wikipedia. Output your thoughts first!")
```

---

## Events You Can Track

Callback handlers can monitor a wide range of events:

### **LLM Events**
- **`on_llm_start`**: Triggered when the LLM begins processing input.
- **`on_llm_end`**: Triggered when the LLM finishes generating a response.
- **`on_llm_chunk`**: Provides real-time output during LLM streaming.

### **Tool Events**
- **`on_tool_start`**: Triggered when a tool (e.g., search) starts executing.
- **`on_tool_end`**: Triggered when a tool completes its task.

### **Agent Events**
- **`on_agent_start`**: Triggered when the agent starts processing a task.
- **`on_agent_end`**: Triggered when the agent concludes the task.

---

## Asynchronous Callbacks

To handle events asynchronously, use `AsyncCallBackHandler`. Here's an example:

```python
from synthora.callbacks import AsyncCallBackHandler

class MyAsyncHandler(AsyncCallBackHandler):
    async def on_llm_start(self, source, messages, **kwargs):
        print("Starting to process...")

    async def on_llm_end(self, source, message, **kwargs):
        print("Processing complete!")
```

---

## Additional Features

### Add Multiple Handlers
You can attach multiple handlers to your agent for different purposes:
```python
agent.add_handler(RichOutputHandler())  # For console output
agent.add_handler(MyCustomHandler())    # For custom logging
```

### Remove Handlers
Handlers can be removed with ease:
```python
agent.remove_handler(handler)
# Or simply use:
agent -= handler
```

### Target Specific Components
Handlers can also be added to specific tools within the agent:
```python
# Add handler to the first tool in the agent's tool list
agent.tools[0].callback_manager.add(handler)
```

---

## Quick Usage Example

For a streamlined setup, you can initialize a default agent with handlers:
```python
agent = VanillaAgent.default(ZeroShotCoTPrompt, handlers=[RichOutputHandler()])
agent.model.set_stream(True)

agent.run("How many letters 'r' are in the word 'strawberry'?")
```

---

### Callback Event Reference Table

| **Event Name**     | **Trigger Timing**                                          | **Parameters Description**                                                                                       |
|--------------------|-------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| **on_llm_start**   | Triggered when the LLM starts processing input.             | `source`: Node initiating the operation<br>`messages`: List of input messages<br>`stream`: Whether streaming is enabled |
| **on_llm_end**     | Triggered when the LLM completes processing.                | `source`: Node initiating the operation<br>`message`: Final output message<br>`stream`: Whether streaming was enabled |
| **on_llm_error**   | Triggered when the LLM encounters an error.                 | `source`: Node where the error occurred<br>`e`: Exception raised<br>`stream`: Whether streaming was enabled       |
| **on_llm_chunk**   | Triggered when the LLM produces a streaming chunk.          | `source`: Node producing the chunk<br>`message`: The chunked output message                                      |
| **on_tool_start**  | Triggered when a tool starts execution.                     | `source`: Node initiating the tool                                                                               |
| **on_tool_end**    | Triggered when a tool completes execution.                  | `source`: Node executing the tool<br>`result`: Result of the tool execution                                      |
| **on_tool_error**  | Triggered when a tool encounters an error.                  | `source`: Node where the error occurred<br>`result`: Error result from the tool                                  |
| **on_agent_start** | Triggered when an agent starts processing.                  | `source`: Node initiating the agent<br>`message`: Initial message for the agent                                  |
| **on_agent_end**   | Triggered when an agent completes processing.               | `source`: Node initiating the agent<br>`message`: Final message from the agent                                   |
| **on_agent_error** | Triggered when an agent encounters an error.                | `source`: Node where the error occurred<br>`result`: Error result from the agent                                 |

This table includes all the callback events and their associated parameters for effective tracking and debugging.

---

### Callback Management with Managers

Callbacks are managed using **AsyncCallBackManager** and **BaseCallBackManager**. These managers allow you to register and handle callback functions for various events, ensuring flexibility and control over how events are processed.

#### Key Points:
1. **AsyncCallBackManager**:
   - Supports both **asynchronous** and **synchronous** callback functions.
   - Provides the ability to handle events in asynchronous contexts.

2. **BaseCallBackManager**:
   - Only supports **synchronous** callback functions.
   - Best suited for simple or non-asynchronous operations.

#### Summary of Differences:
| **Manager**               | **Supports Sync Callbacks** | **Supports Async Callbacks** |
|---------------------------|----------------------------|-----------------------------|
| **AsyncCallBackManager**  | ✅                         | ✅                          |
| **BaseCallBackManager**   | ✅                         | ❌                          |

By choosing the appropriate callback manager for your use case, you can ensure smooth event handling and proper integration with your agent’s workflow.

---

### Summary

Synthora's callback system provides a powerful mechanism to track and manage events in your agent's lifecycle. By leveraging callbacks, you gain deep insights into the agent’s operations, including LLM processing, tool usage, and overall task execution. Here’s a recap of the key takeaways:

1. **Comprehensive Event Tracking**:
   - Monitor events such as LLM start, tool execution, agent tasks, and errors with detailed callbacks.

2. **Flexible Integration**:
   - Use **BaseCallBackHandler** for synchronous callbacks or **AsyncCallBackHandler** for asynchronous workflows.
   - Easily customize behavior by implementing your own callback functions.

3. **Powerful Managers**:
   - **AsyncCallBackManager** supports both synchronous and asynchronous callbacks.
   - **BaseCallBackManager** is restricted to synchronous callbacks, ensuring compatibility in simpler scenarios.

4. **Ease of Use**:
   - Add or remove handlers effortlessly.
   - Target specific components like tools or agents for precise tracking.

By integrating Synthora’s callback system into your agents, you can enhance debugging, optimize performance, and create a more transparent and robust AI-driven system. Choose the right callback tools and managers to suit your project’s needs, and unlock the full potential of your agent workflows!
