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

# Introduction to `Synthora`

## What's an Agent Framework?

An agent framework is a higher-level abstraction built on top of foundational LLM (Large Language Model) capabilities. Its primary goal is to simplify development, reduce repetitive tasks, and enhance user productivity. Agent frameworks serve as the connective tissue between raw language models and complex, real-world applications by:

- **High-level Encapsulation**: Wrapping around LLMs to provide pre-built functionalities like reasoning chains, decision-making logic, and task planning.
- **Streamlining Repetitive Tasks**: Automating workflows, such as input parsing, tool integration, and response generation.
- **Enabling Customization**: Offering a modular structure so developers can extend or replace components without reinventing the wheel.
- **Enhancing Productivity**: Providing ready-to-use patterns (e.g., conversational agents, task-specific agents) that allow developers to focus on macro-level objectives.

---

## What Makes `Synthora` Different?

`synthora` is a lightweight agent framework designed to balance simplicity and functionality, enhancing the overall user experience.

We believe a good agent framework should reduce the workload for developers by automating repetitive and complex tasks, making development easier and more efficient.
Our goal is to offer a solution that is as lightweight as possible while still being fully functional.

### The Problem with Existing Frameworks

Existing agent frameworks often come with a plethora of features but tend to become cumbersome when users need to make modifications. Once these frameworks fail to meet specific requirements, their complex and tightly coupled codebases make customization and maintenance a challenging task.

### Our Philosophy

Instead of attempting to provide every possible feature in a single framework, we prioritize **customizability** and **simplicity**. This means that if the existing components don’t meet your needs, you can easily extend our components and adapt them to your requirements. This philosophy is reflected in the streamlined design of `Synthora`, which minimizes unnecessary abstractions and bloated code.

### Customization Made Easy

In most cases, users only need to focus on high-level logic. By modifying just one or two key functions in our existing components, users can achieve their desired functionality without dealing with unnecessary complexity. Our aim is to make customization as intuitive and straightforward as possible.

### Why Choose `Synthora`?

- **Minimalist Core**: By keeping the framework lightweight, we provide a solid foundation that doesn’t impose unnecessary constraints or overhead.
- **Focus on Modularity**: Every component in `Synthora` is designed to be extensible. Whether it's agents, tools, workflows, or models, you can tailor each part to fit your specific use case.
- **Encourage User Innovation**: Instead of overloading the framework with features, we empower users to create their own solutions using our extensible components.

By offering a framework that emphasizes flexibility, simplicity, and ease of customization, `Synthora` is built to enable users to focus on building innovative solutions without being bogged down by unnecessary complexity.

---

## Core Features of `Synthora`

### **Agents**
`Synthora` offers a comprehensive agent framework with support for various predefined agent types such as **COT (Chain of Thought)**, **TOT (Tree of Thought)**, and **ReAct (Reasoning and Action)**. These agents can operate independently or collaboratively in multi-agent systems.

You can also define and manage **multi-agent interactions** through configuration files or straightforward code, enabling complex task orchestration with ease.

### **Tools**
Tools are essential for empowering agents to interact with external systems. `Synthora` provides multiple methods to convert Python functions or classes into tools that agents can invoke. While `Synthora` includes a basic set of tools, it encourages users to integrate with other open-source toolkits or develop custom tools tailored to their needs.

### **Workflows**
A robust workflow system is at the heart of `Synthora`. Users can define complex workflows that support:
- **Parallel** and **Sequential Execution**
- **Loops** and **Conditional Branches**

This allows you to automate intricate processes and meet the demands of diverse scenarios.

---

## Key Advantages

### **Simple**
`Synthora` is designed for simplicity. It avoids unnecessary abstractions and deep nesting, ensuring a low learning curve. It's ready to use right out of the box.

### **Unified Interface**
All inputs and outputs for models and agents in `Synthora` adhere to the `BaseMessage` format—no exceptions. Similarly, for agents and tools, all return values follow the `Result` generic pattern (`Ok` or `Err`, inspired by Rust), making the behavior consistent and predictable.

### **Flexible**
Every component in `Synthora` is extensible or independently usable. If something doesn’t meet your requirements, simply replace it with your implementation. `Synthora` is optimized to make this process easy and intuitive.

### **Complete Sync & Async Support**
From agents and models to tools, callbacks, and workflows, `Synthora` supports both synchronous and asynchronous operations. This ensures you can build performant applications regardless of your requirements.

### **Serialization-Ready**
Serialization is a core consideration in `Synthora`. In most cases, you can construct agents entirely from configuration files (e.g., YAML) without writing a single line of Python code. This enables:
- Easier sharing of pre-configured agents.
- Enhanced security for agent hosting by avoiding Python file uploads.
- Nested configuration support for even the most complex setups.

---

By prioritizing flexibility, simplicity, and functionality, `Synthora` empowers developers to build intelligent systems faster, better, and with less hassle. Whether you’re a seasoned developer or new to agent frameworks, `Synthora` provides the tools you need to get started and scale.
