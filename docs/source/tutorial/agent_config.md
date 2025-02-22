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

# Create Your First Agent in Minutes! 🚀

Want to build your own AI agent? With Synthora, it's as easy as creating simple YAML files! Let's start with a basic version and then add more capabilities.

## Basic Version: Simple Conversational Agent 💬

### What You'll Need ✨
Just two configuration files:
1. An agent config file (defines agent behavior)
2. A model config file (sets up the AI model)

### 1️⃣ Agent Configuration (basic_agent.yaml)
```yaml
name: basic-assistant
type: vanilla
model: !include basic_model.yaml  # Points to your model config
prompt: "You are an AI Assistant. You are here to help me with my queries."
```

### 2️⃣ Model Configuration (basic_model.yaml)
```yaml
name: basic-model
model_type: gpt-4
backend: openai_chat
backend_config:
  api_key: "your-api-key"
config:
  temperature: 0
  top_p: 1.0
  stream: true
```

### Let's Try It! 🎮
```python
from synthora.agents import VanillaAgent
from synthora.configs import AgentConfig
from synthora.callbacks import RichOutputHandler

# Load your agent's configuration
config = AgentConfig.from_file("examples/agents/configs/basic_agent.yaml")

# Create your agent with nice output formatting
agent = VanillaAgent.from_config(config)
handler = RichOutputHandler()
agent.add_handler(handler)

# Start chatting!
agent.run("What is artificial intelligence?")
```

## Advanced Version: Adding Search Capabilities 🔍

Let's upgrade our agent by adding search capabilities! Here's how:

### 1️⃣ Enhanced Agent Configuration (search_agent.yaml)
```yaml
name: search-assistant
type: vanilla
model: !include basic_model.yaml
prompt: "You are an AI Assistant with search capabilities. You can search the web to answer questions."
tools:
  - synthora.toolkits.search_toolkit.SearchToolkit  # Adds search functionality! 🔍
```

The model configuration remains the same, but now your agent can search the web!

### Try Your Enhanced Agent! 🚀
```python
# Load the enhanced configuration
config = AgentConfig.from_file("examples/agents/configs/search_agent.yaml")

# Create your search-capable agent
agent = VanillaAgent.from_config(config)
handler = RichOutputHandler()
agent.add_handler(handler)

# Test the search functionality
agent.run("Search OpenAI on Wikipedia")
```

## What Makes It Special? ⚡

- **Simple Setup**: Start with basic chat and add tools as needed
- **Powerful AI**: Powered by OpenAI's GPT-4
- **Extensible**: Easy to add more capabilities
- **Beautiful Output**: Clean formatting to track agent actions

That's it! You've learned how to create both a basic chatbot and a search-capable AI agent. Amazing what a few lines of code can do! 😎
