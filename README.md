<!-- LICENSE HEADER MANAGED BY add-license-header

Copyright 2024-2025 Syntropix-AI.org

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

# Synthora
[![Read the Docs](https://img.shields.io/readthedocs/synthora)](https://docs.syntropix.ai/)


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
- 🔧 Powerful workflows to assist in accomplishing diverse tasks.

## Installation

To install Synthora Python Library from PyPI, simply run:

```shell Shell
pip install synthora
```

## What Makes Synthora Different

Existing agent frameworks are too heavy. We aim to provide users with a solution that is as lightweight as possible while remaining fully functional.

Synthora provides most of the core features you need, such as **Agents**, including various types of predefined agents (e.g., COT, TOT, ReAct, etc.).
It also offers a **multi-agent interaction framework**, allowing users to combine multiple agents through configuration files or simple code.
As for **Tools**, Synthora provides multiple ways to convert functions or classes into forms that agents can call. Synthora itself only offers the most basic tools.
We encourage users to leverage tools from other open-source projects or create custom tools.
Finally, there’s **Workflow**. Synthora provides a powerful workflow system that allows users to define complex workflows. Workflows support parallel and sequential operations, as well as loops and branches, meeting the needs of most scenarios.

At present, Synthora does not support **Retrieval**. Many retrieval libraries already exist, offering robust features that Synthora is unlikely to surpass.
However, these libraries can be easily integrated with Synthora. All you need to do is treat them as a tool or use a sequential workflow to obtain retrieval results.


## Quick Start

### Chat with Agent

```python

from synthora.callbacks import RichOutputHandler
from synthora.agents import VanillaAgent

agent = VanillaAgent.default("You are a Vanilla Agent.", handlers=[RichOutputHandler()])
agent.run("Hi! How are you?")
```

### Define Tools

```python
from synthora.toolkits.decorators import tool


@tool
def add(a: int, b: int) -> int:
    r"""Add two numbers together."""
    return a + b
```

### Workflow

```python
def add(x: int, y: int) -> int:
    return x + y

flow = (BaseTask(add) | BaseTask(add)) >> BaseTask(add)
flow.run(1, 2)
```
