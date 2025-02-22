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

# First Steps with `Synthora`

Here’s how you can get started with `Synthora` to build powerful and flexible agents:

```python
from synthora.agents import VanillaAgent

agent = VanillaAgent.default()
print(agent.run("Hi! How are you?").unwrap())
```

### Understanding the `VanillaAgent`

- **`VanillaAgent`**: This is the simplest agent provided by `Synthora`. It is an excellent starting point for basic interactions.
- **Return Value**: If everything works correctly, the agent's return value will be `Ok(BaseMessage)`.
- **Accessing Text Content**: The `BaseMessage` contains complete information about the response. If you only need the text content, you can access it directly:

  ```python
  print(agent.run("Hi! How are you?").unwrap().content)
  ```

---

### Improving Output Presentation

Simply printing the response to the command line might suffice for basic testing, but it can get unwieldy when dealing with more extensive content. `Synthora` provides predefined **callbacks** to help you present information in a structured and visually appealing way.

For example, you can use the `RichOutputHandler` for better output formatting:

```python
from synthora.agents import VanillaAgent
from synthora.callbacks import RichOutputHandler

agent = VanillaAgent.default("Your name is Synthora", handlers=[RichOutputHandler()])
agent.run("Hi! How are you?")
```

Bingo! You’ll notice that everything looks much more organized and easier to read.

---

### Using Custom System Messages

You can also customize the **system message** to guide the agent's behavior. The system message acts as the "persona" or instructions for the agent, telling it how to respond to user input. For example:

```python
agent = VanillaAgent.default("Your name is Synthora, and you are here to assist with technical queries.", handlers=[RichOutputHandler()])
agent.run("What is Synthora?")
```

---

### Advanced Agents: CoT, ReAct, and More

For more complex tasks, the `VanillaAgent` might not suffice. `Synthora` makes it easy to switch to advanced agents like **CoT (Chain-of-Thought)** or **ReAct (Reasoning and Action)** agents:

```python
from synthora.agents import ReactAgent
from synthora.callbacks import RichOutputHandler
from synthora.prompts.buildin import ZeroShotCoTPrompt

# Using a React Agent
agent = ReactAgent.default("You are a React Agent.")
print(agent.run("Hi! How are you?").unwrap().content)

# Using a Chain-of-Thought Prompt
agent = VanillaAgent.default(ZeroShotCoTPrompt)
print(agent.run("How many letters 'r' are in the word 'strawberry'?").unwrap().content)
```

---

### Empowering Agents with Tools

To handle more sophisticated tasks, agents need tools. `Synthora` makes it simple to add tools to your agents.

#### Predefined Tools

`Synthora` provides several predefined tools, such as file manipulation and web search:

```python
from synthora.agents import VanillaAgent
from synthora.callbacks import RichOutputHandler
from synthora.toolkits.file_toolkit import FileToolkit
from synthora.toolkits.search_toolkit import search_all

write_file = FileToolkit.write_file
list_directory = FileToolkit.list_directory

agent = VanillaAgent.default(
    tools=[search_all, write_file, list_directory],
    handlers=[RichOutputHandler()],
)
```

#### Custom Tools

You can also define your own tools effortlessly using `Synthora`'s decorator-based approach:

```python
from synthora.agents import VanillaAgent
from synthora.toolkits.decorators import tool
from synthora.callbacks import RichOutputHandler

@tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

agent = VanillaAgent.default(
    tools=[add],
    handlers=[RichOutputHandler()],
)
agent.run("123 + 321 = ?")
```

The ability to integrate both predefined and custom tools allows agents to tackle a wide range of real-world problems seamlessly.

---

With `Synthora`, building, customizing, and extending intelligent agents is intuitive and efficient. Start simple with `VanillaAgent` and scale up to more advanced agents and tools as your needs evolve.
