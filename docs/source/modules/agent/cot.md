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

# Chain-of-Thought (CoT) Agent

The **Chain-of-Thought (CoT) Agent** in Synthora is not a separate class but a configuration of the `VanillaAgent` with a specialized **prompt**. By using the `ZeroShotCoTPrompt`, the agent is guided to perform step-by-step reasoning, enabling it to solve problems that require logical breakdowns or intermediate steps.

---

## Overview

### Purpose
- The CoT Agent leverages **Chain-of-Thought prompting** to explicitly generate intermediate steps in its reasoning process.
- It builds on the `VanillaAgent` while providing additional capabilities for structured reasoning.

### Key Features
1. **Step-by-Step Reasoning**: Breaks problems into smaller, manageable reasoning steps.
2. **Predefined Prompt**: Utilizes a specialized `ZeroShotCoTPrompt` for CoT reasoning.

---

## Implementation

Here is how the CoT Agent is created and used:

### Code Example

```python
from synthora.agents import VanillaAgent
from synthora.callbacks import RichOutputHandler
from synthora.prompts.buildin import ZeroShotCoTPrompt

# Create a CoT Agent with step-by-step reasoning
agent = VanillaAgent.default(
    ZeroShotCoTPrompt,
    handlers=[RichOutputHandler()]  # Adds rich output formatting
)

# Enable streaming for real-time output
agent.model.set_stream(True)

# Execute a reasoning task
response = agent.run("How many letters 'r' in the word 'strawberry'?")
print(response.unwrap())  # Outputs: "The word 'strawberry' contains 3 letters 'r'."
```

---

## Example Walkthrough

### Input
```plaintext
How many letters 'r' in the word 'strawberry'?
```

### Reasoning Steps (CoT Output)
1. The word is "strawberry".
2. Count the occurrences of the letter 'r':
   - First 'r' in position 4.
   - Second 'r' in position 8.
   - Third 'r' in position 9.
3. There are 3 'r's in the word "strawberry".

### Final Output
```plaintext
The word "strawberry" contains 3 letters 'r'.
```

---

## Key Advantages of the CoT Agent

1. **Enhanced Problem-Solving**:
   - CoT reasoning improves accuracy on tasks that benefit from intermediate steps.

2. **Transparency**:
   - Provides insights into the reasoning process, making it easier to debug and validate results.

---

## Summary

The **Chain-of-Thought (CoT) Agent** is a powerful extension of the Synthora framework, tailored for tasks requiring logical breakdowns and reasoning transparency. By integrating step-by-step reasoning, predefined prompts, and rich output formatting, it provides a robust tool for solving complex problems in an intuitive and explainable manner.
