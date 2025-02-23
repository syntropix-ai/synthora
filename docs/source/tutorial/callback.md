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

# Level Up Your Agent with Callbacks! 🎯

Want to see what's happening inside your agent's mind? Synthora's callback system lets you peek behind the curtain! Let's explore how to add awesome logging and event tracking to your agent.

## What Are Callbacks? 🤔

Think of callbacks as little reporters that tell you what's happening at every step:
- When your agent starts thinking
- When it uses tools
- When it makes decisions
- Even when something goes wrong!

## Adding Callbacks is Super Easy! ✨

Here's how to add beautiful console output to your agent in just a few lines:

```python
from synthora.agents import ReactAgent
from synthora.configs import AgentConfig
from synthora.callbacks import RichOutputHandler

# Create your agent
config = AgentConfig.from_file("examples/agents/configs/react_agent.yaml")
agent = ReactAgent.from_config(config)

# Add pretty console output with just two lines! ✨
handler = RichOutputHandler()
agent.add_handler(handler)

# Watch the magic happen!
agent.run("Search OpenAI on Wikipedia. Output your thoughts first!")
```

## What Can You Track? 🔍

Your callback handler can listen to all these cool events:

- **LLM Events**:
  - `on_llm_start`: When the LLM starts processing
  - `on_llm_end`: When the LLM completes its response
  - `on_llm_chunk`: Real-time output during LLM streaming!

- **Tool Events**:
  - `on_tool_start`: When a tool (like search) kicks in
  - `on_tool_end`: When the tool finishes its job

- **Agent Events**:
  - `on_agent_start`: When your agent begins a task
  - `on_agent_end`: When it completes the mission

## Want Async? We've Got You Covered! ⚡

Need to handle events asynchronously? Just use `AsyncCallBackHandler`:

```python
from synthora.callbacks import AsyncCallBackHandler

class MyAsyncHandler(AsyncCallBackHandler):
    async def on_llm_start(self, source, messages, **kwargs):
        print("🤔 Starting to think...")

    async def on_llm_end(self, source, message, **kwargs):
        print("💡 Got it!")
```

## Pro Tips! 💡

1. You can add multiple handlers:
```python
agent.add_handler(RichOutputHandler())  # For console output
agent.add_handler(MyCustomHandler())    # For custom logging
```

2. Remove handlers just as easily:
```python
agent.remove_handler(handler)  # Or use agent -= handler
```

3. Track specific components:
```python
# Add handler to just the search tool
agent.tools[0].callback_manager.add(handler)
```

That's it! Now you can watch your agent think, search, and solve problems in real-time. How cool is that? 🌟

Want to learn more? Check out our [advanced callbacks documentation](https://synthora.readthedocs.io/)!
