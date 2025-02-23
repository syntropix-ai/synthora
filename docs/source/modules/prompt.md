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

# Prompt

The `Prompt` functionality in `synthora` provides a way to create and manage customizable prompt templates with dynamic argument formatting. This system integrates with agents like `VanillaAgent` and allows for flexible prompt handling during runtime.

---

## Example Usage

Here is an example of how to use `BasePrompt` with a `VanillaAgent`:

```python
from synthora.agents.vanilla_agent import VanillaAgent
from synthora.callbacks import RichOutputHandler
from synthora.prompts import BasePrompt

# Define a prompt template
prompt = BasePrompt("Your name is {username}.")

# Create a default VanillaAgent using the prompt and a callback handler
agent = VanillaAgent.default(prompt, handlers=[RichOutputHandler()])

# Run the agent with input and a template argument
agent.run("what is your name?", username="John Doe")
```

### Output
The agent will dynamically replace `{username}` in the prompt with `"John Doe"` and process the query accordingly.

---

## BasePrompt Class

The `BasePrompt` class extends Python’s built-in `str` class, adding functionality for working with template strings and argument validation.

### Key Features

1. **String-like Behavior**
   - `BasePrompt` is a subclass of `str`, so it behaves like a standard string.

2. **Template Argument Extraction**
   - Dynamically extracts placeholder arguments from a template.

3. **Safe Formatting**
   - Validates arguments against the template and only substitutes recognized placeholders.

4. **Integration with Pydantic**
   - Supports serialization through Pydantic for seamless configuration handling.

---

### Properties and Methods

#### `args` (Property)

Extracts all unique placeholders (arguments) in the prompt template.

##### Example
```python
prompt = BasePrompt("Your name is {username} and your role is {role}.")
print(prompt.args)  # Output: {'username', 'role'}
```

#### `format` (Method)

Formats the prompt template by substituting placeholders with the provided arguments. It ensures that only the placeholders present in the template are replaced.

##### Parameters
- `**kwargs`: Key-value pairs for substituting template placeholders.

##### Example
```python
prompt = BasePrompt("Your name is {username}.")
formatted_prompt = prompt.format(username="Alice")
print(formatted_prompt)  # Output: "Your name is Alice."
```

---

### Built-in Prompts

The following table summarizes the built-in prompts provided in `synthora`, their purposes, and typical use cases:

| **Prompt Name**              | **Description**                                                                                   | **Use Case**                                                                                  |
|-------------------------------|---------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| `ZeroShotCoTPrompt`          | A prompt designed for zero-shot chain-of-thought reasoning, encouraging step-by-step explanations. | Use when requiring the model to provide detailed reasoning without prior examples.          |
| `ZeroShotReactPrompt`        | A zero-shot prompt for reasoning and acting (ReAct) in tasks requiring a mix of analysis and action.| Suitable for scenarios requiring both reasoning and action, without additional examples.     |
| `FewShotReactPrompt`         | A few-shot ReAct prompt providing the model with examples to guide reasoning and action.           | Use when examples improve performance in reasoning and acting tasks.                        |
| `ZeroShotTOTProposePrompt`   | A zero-shot Tree-of-Thought (ToT) prompt for proposing multiple reasoning paths.                   | Ideal for brainstorming or exploring diverse problem-solving approaches.                    |
| `ZeroShotTOTEvalPrompt`      | A zero-shot ToT evaluation prompt for assessing and ranking proposed solutions or ideas.           | Use when evaluating multiple proposed solutions to select the best one.                     |
| `VanillaPrompt`              | A simple, general-purpose prompt template for straightforward interactions.                        | Suitable for standard queries where minimal guidance is required.                           |

These prompts are pre-configured to cover a wide range of interaction styles and can be customized further as needed for specific applications.

---

## Summary

The `BasePrompt` class provides a robust and extensible way to handle dynamic prompt templates in `synthora`. By leveraging its integration with agents, templates, and Pydantic, it simplifies the process of creating personalized and context-aware AI interactions.
