<!-- LICENSE HEADER MANAGED BY add-license-header

=========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
Licensed under the Apache License, Version 2.0 (the “License”);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
=========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
-->

# Synthora Documentation

Welcome to Synthora's documentation!

Synthora is a lightweight and extensible framework for LLM-driven Agents and ALM research. It provides essential components to build, test and evaluate agents. At its core, Synthora aims to assemble an agent with a single config, thus minimizing your effort in building, tuning, and sharing agents.

Note: This project is in its very early stages of development. The APIs are unstable and subject to significant changes, which may introduce breaking updates. Use with caution, as there are inherent risks in adopting this framework at its current maturity level. Feedback and contributions are welcome to help improve its stability and functionality.

## Motivation 🧠
Agent practitioners start to realize the difficulty in tuning a "well-rounded" agent with tons of tools or instructions in a single layer.
Recent studies like [TinyStories](https://arxiv.org/abs/2301.12726), [Specializing Reasoning](https://arxiv.org/abs/2301.12726), [Let's Verify SbS](https://arxiv.org/abs/2305.20050), [ReWOO](https://arxiv.org/abs/2305.18323), etc. also point us towards an intuitive yet undervalued direction 👉

```
An LLM is more capable if you create a context/distribution shift specialized to some target tasks.
```
Sadly, there is no silver bullet for agent specialization. For example, you can
- Simply add `Let's think step by step.` in your **prompt** for more accurate Math QA.
- Give a **few-shot** exemplar in your prompt to guide a better reasoning trajectory for novel plotting.
- Supervise **fine-tuning** (SFT) your 70B `llama2` like [this](https://arxiv.org/abs/2305.20050) to match reasoning of 175B GPT-3.5.
- And more ...

Isn't it beautiful if one shares his effort in specialized intelligence, allowing others to reproduce, build on, or interact with it? 🤗 This belief inspires us to build Synthora,
**designed for agent *specialization, sharing, and interaction,* to stackingly achieve collective growth towards greater intelligence.**.

## Core Features 💡

- ⚙️ Config-driven agent assembling and chat.
- 🚀 Large amount of prebuilt agent types, LLM clients, tools, memory systems, and more.
- 🪶 Lightweight and highly extensible implementation of essential components.
- 🧪 Aligning with state-of-the-art AI research.
- 🤝 Enabling multi-agent interactions.
- 🦁 Unique platform of agent zoo and eval benchmark.

## Installation

To install Synthora Python Library from PyPI, simply run:

```shell Shell
 pip install synthora
```

## Quick Start


```python

from synthora.agents import VanillaAgent
from synthora.configs import AgentConfig
from synthora.callbacks import RichOutputHandler

import warnings
warnings.filterwarnings("ignore")

config = AgentConfig.from_file("examples/agents/configs/vanilla_agent.yaml")

agent = VanillaAgent.from_config(config)
handler = RichOutputHandler()
agent.tools[0].callback_manager.add(handler)
agent.model.callback_manager.add(handler)
agent.callback_manager.add(handler)

agent.run("Search Openai on Wikipedia")
```

```{toctree}
:caption: Tutorial
:maxdepth: 2
:hidden:

tutorial/config
tutorial/callback
```

```{toctree}
:caption: Examples
:maxdepth: 2
:hidden:

cookbook/chat_with_agent.ipynb
```

```{toctree}
:caption: Contents
:maxdepth: 2
:hidden:

synthora.agents
synthora.configs
synthora.messages
synthora.models
synthora.prompts
synthora.toolkits
synthora.callbacks
synthoraa.tracers
synthora.types
synthora.utils
synthora
```
