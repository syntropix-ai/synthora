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

# Tree-of-Thought (ToT) Agent

The **ToT Agent** (Tree-of-Thought Agent) is an advanced implementation in the Synthora framework designed for incrementally solving complex problems. It employs a tree-based exploration strategy, enabling the agent to evaluate multiple reasoning paths and refine its approach iteratively.

---

## Overview

### Purpose
- ToT Agents leverage a **tree-based search strategy** to systematically explore and evaluate multiple solutions to a problem.
- This approach allows for iterative refinement of ideas, enabling better decision-making.

### Key Features
1. **Tree-of-Thought Exploration**:
   - Supports both depth-first (DFS) and breadth-first (BFS) search methods for navigating the solution tree.
2. **Iterative Reasoning**:
   - Proposes solutions, evaluates them, and refines or discards paths based on scores.
3. **Multiple Models**:
   - Uses two models: one for proposing solutions and another for evaluating them.
4. **Threshold Control**:
   - Supports `finish_threshold` to determine when a solution is acceptable and `giveup_threshold` to abandon low-quality paths.
5. **Customizable Levels**:
   - Configurable `level_size` and `max_turns` for fine-grained control over search depth and breadth.

---

## Implementation

### Code Example

```python
from synthora.agents.tot import ToTAgent

# Create a ToT Agent with specified parameters
agent = ToTAgent.default(
    model_type="gpt-4o",   # Use GPT-4 optimized model
    max_turns=15,          # Maximum reasoning steps
    level_size=2,          # Number of nodes per level in the search tree
    giveup_threshold=0.2,  # Threshold for abandoning paths
)

# Process a query
response = agent.run("How many r's are there in the word 'strawberry'?")
print(response.unwrap())  # Example output: "There are 3 r's in 'strawberry'."

# Print the history of reasoning
for i in agent.history[1:]:
    print(i.content)
```

---

### Components

#### 1. **Models**
- **Propose Model**:
  - Generates potential solutions or actions.
- **Value Model**:
  - Evaluates the quality of proposed solutions, assigning scores and reasons.

#### 2. **Prompts**
- **`ZeroShotTOTProposePrompt`**:
  - Used by the propose model to generate new ideas or solutions.
- **`ZeroShotTOTEvalPrompt`**:
  - Used by the value model to evaluate the generated ideas.

#### 3. **Thresholds**
- **Finish Threshold (`finish_threshold`)**:
  - Determines the minimum score required for a solution to be accepted.
- **Giveup Threshold (`giveup_threshold`)**:
  - Defines the minimum score required to continue exploring a branch.

#### 4. **Search Method**
- Supports **DFS** (Depth-First Search) and **BFS** (Breadth-First Search) for navigating the tree of solutions.

---

## Key Methods

#### `default()`
Creates a default ToT Agent with pre-configured parameters.

**Arguments**:
- `propose_prompt` (str): The propose model prompt template.
- `value_prompt` (str): The value model prompt template.
- `level_size` (int): Number of nodes to expand at each level.
- `max_turns` (int): Maximum number of iterations.
- `finish_threshold` (float): Minimum score for solution acceptance.
- `giveup_threshold` (float): Minimum score for continuing exploration.
- `search_method` (str): Tree traversal strategy ("dfs" or "bfs").
- `model_type` (str): The type of model to use.

**Returns**:
- An instance of `ToTAgent`.

---

#### `step()`
Executes a single step of the reasoning and action loop:
1. Proposes multiple solutions using the propose model.
2. Evaluates the solutions using the value model.

**Arguments**:
- `message` (str or BaseMessage): Input message to process.

**Returns**:
- A `Result` containing proposed solutions and evaluations.

**Example**:
```python
response = agent.step("What is 15% of 120?")
print(response.unwrap())  # Outputs intermediate solutions and evaluations.
```

---

#### `run()`
Performs the full reasoning and action loop until:
1. A satisfactory solution is found (`finish_threshold` reached).
2. The maximum number of turns (`max_turns`) is reached.

**Arguments**:
- `message` (str or BaseMessage): Input query.

**Returns**:
- A `Result` containing the final solution or an error.

**Example**:
```python
response = agent.run("What are the prime factors of 28?")
print(response.unwrap())  # Outputs: "The prime factors of 28 are 2 and 7."
```

---

#### `add_tool()` and `remove_tool()`
- Dynamically add or remove tools for enhanced functionality.

**Example**:
```python
# Add a tool
agent.add_tool(my_custom_tool)

# Remove a tool
agent.remove_tool(my_custom_tool)
```

---


## Summary

The **ToT Agent** leverages the Tree-of-Thought framework to solve problems through structured exploration and evaluation. By integrating two models for proposing and evaluating solutions, it enables iterative reasoning and refinement. With configurable thresholds and tree traversal strategies, the ToT Agent is ideal for complex, multi-step tasks requiring logical breakdowns and systematic problem-solving.
