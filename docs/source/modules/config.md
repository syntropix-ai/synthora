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

# Config

## Overview

In `synthora`, configurations are defined using YAML files, enabling a modular and reusable approach to setting up models, agents, and tools. Below is a detailed explanation of the configurations and their use cases.

---

### **Basic Model Configuration**
The `basic_model.yaml` file defines the foundational configuration for a model.

```yaml
name: gpt-4o
backend: openai
backend_config:
  api_key: YOUR_API_KEY
  url: https://api.openai.com
config:
  temperature: 0
  top_p: 1.0
```

#### Key Parameters:
- **`name`**: The name of the model, here `gpt-4o`.
- **`backend`**: Specifies the backend provider, such as `openai`.
- **`backend_config`**: Contains the necessary configuration for the backend, like API keys and endpoint URLs.
- **`config`**: Defines model-specific parameters like `temperature` and `top_p` for controlling response randomness and diversity.

---

### **Referencing a Model Configuration in an Agent**
The `basic_agent.yaml` file demonstrates how to use the `basic_model.yaml` configuration in an agent.

```yaml
name: test
type: vanilla
model: !include basic_model.yaml
prompt: "Your name is {x}"
```

#### Key Parameters:
- **`name`**: The name of the agent, here `test`.
- **`type`**: The type of the agent, such as `vanilla`.
- **`model`**: References the model configuration using `!include basic_model.yaml`.
- **`prompt`**: The agent-specific prompt template, e.g., `"Your name is {x}"`.

#### Loading the Agent Configuration:
You can load the agent configuration programmatically:
```python
config = AgentConfig.load("YOUR_PATH/basic_agent.yaml")
```

---

### **Using an Agent as a Tool**
The `vanilla_agent.yaml` file demonstrates how to embed an agent within another agent or toolkit.

```yaml
name: Vanilla
type: vanilla
model: !include basic_model.yaml
prompt: "You are an AI Assistant. You are here to help me with my queries. Your name is vanilla."
tools:
  - synthora.toolkits.basic_math_toolkit.BasicMathToolkit
  - target: synthora.agents.VanillaAgent
    args: !include basic_agent.yaml
```

#### Key Additions:
- **`tools`**: Specifies tools or other agents that the current agent can use.
  - **`synthora.toolkits.basic_math_toolkit.BasicMathToolkit`**: A toolkit providing basic math functionalities.
  - **`target`**: Points to another agent class, here `synthora.agents.VanillaAgent`.
  - **`args`**: Includes configuration for the target agent using `!include`.

---

### **Referencing Predefined Prompts**
The `searcher.yaml` file illustrates how to use predefined prompts.

```yaml
name: WebSearcher
description: "This agent is a simple AI assistant that can help you search the web."
type: react
model: !include basic_model.yaml
prompt: !prompt FewShotReactPrompt
```

#### Highlights:
- **`prompt`**: Uses `!prompt` to reference a predefined prompt (`FewShotReactPrompt`), allowing for prompt standardization across agents.

---

### **Building an Agent from Config**
To construct an agent using its configuration, you can use the appropriate agent class and call the `from_config` method. The class is determined by the `type` of the agent.

#### Example:
For a `VanillaAgent`:
```python
agent = VanillaAgent.from_config(config)
```

---

This configuration-based setup ensures flexibility, reusability, and a clear separation of concerns, allowing you to define, extend, and manage agents and tools efficiently.
