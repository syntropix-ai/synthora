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

### Toolkit

In Synthora, **Tools** are fundamental units of functionality exposed to agents. These tools can be synchronous or asynchronous and are designed to provide well-defined actions or computations as part of the agent framework. Tools facilitate structured and extensible interactions by following a standardized schema.

#### Key Concepts of Tools in Synthora:

1. **Purpose of Tools**:
   - Tools encapsulate specific functionalities, enabling agents to interact with them in a modular way.
   - They support callback mechanisms, allowing event-driven execution and result tracking.

2. **Initialization**:
   - Tools are created using the `@tool` decorator. This decorator wraps a function or method and ensures it adheres to the framework's structure, handling both synchronous (`SyncFunction`) and asynchronous (`AsyncFunction`) execution patterns.

---

### Tool Definition Using the `@tool` Decorator

The `@tool` decorator marks a function or method as a tool within the Synthora framework. It is the entry point for defining tools and ensures that functions are correctly wrapped for synchronous or asynchronous execution.

#### How It Works:
- **Signature Inspection**:
  The decorator inspects the function's signature to determine if it is a method (i.e., part of a class) by checking for the `self` parameter.

- **Flagging for Methods**:
  If the function is a method, it is marked for later association with its class instance.

- **Tool Wrapping**:
  The function is passed to `BaseFunction.wrap()` for further processing, which creates either a `SyncFunction` or `AsyncFunction` object based on the function's nature (synchronous or asynchronous).

#### Example:
```python
# Synchronous tool definition
@tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers and returns the result."""
    return a + b

# Asynchronous tool definition in a class
class MathTools:
    @tool
    async def multiply_numbers(self, a: int, b: int) -> int:
        """Multiplies two numbers asynchronously."""
        return a * b
```

---

### `BaseFunction`: Abstract Base for Tool Wrappers

The `BaseFunction` class is an abstract base class used to wrap tools. It provides the foundation for both `SyncFunction` and `AsyncFunction` implementations.

#### Responsibilities:
1. **Schema Integration**:
   - Extracts schema metadata for tools (name, description, and parameters) to ensure compatibility with OpenAI tool standards.

2. **Callback Management**:
   - Integrates with callback handlers for events like `TOOL_START`, `TOOL_ERROR`, and `TOOL_END`.

3. **Execution Interfaces**:
   - Provides abstract methods for execution (`__call__`, `run`, and `async_run`) that are implemented in the concrete subclasses.

#### Example Usage:
```python
# Accessing tool metadata and executing
tool_instance = SyncFunction(None, add_numbers)
print(tool_instance.name)  # Prints the tool's name from its schema
result = tool_instance.run(3, 5)  # Executes the tool and handles callbacks
```

---

### Subclasses: `SyncFunction` and `AsyncFunction`

#### `SyncFunction`:
- Handles execution of synchronous functions.
- Supports callback handling during execution (`run` method).
- Raises `NotImplementedError` if asynchronous execution (`async_run`) is attempted.

#### `AsyncFunction`:
- Handles execution of asynchronous functions.
- Allows callbacks during asynchronous execution (`async_run` method).
- Raises `NotImplementedError` if synchronous execution (`run`) is attempted.

---

### Managing Tools with `BaseToolkit`

The `BaseToolkit` class is an abstract base class for managing collections of tools within the framework.

#### Features:
1. **Automatic Tool Collection**:
   - Scans class definitions for methods wrapped with `@tool`.
   - Collects and categorizes them as synchronous or asynchronous tools.

2. **Categorization**:
   - `sync_tools`: List of all synchronous tools.
   - `async_tools`: List of all asynchronous tools.

#### Example:
```python
class MathToolkit(BaseToolkit):
    @tool
    def add(self, a: int, b: int) -> int:
        return a + b

    @tool
    async def subtract(self, a: int, b: int) -> int:
        return a - b

# Usage
toolkit = MathToolkit()
sync_tools = toolkit.sync_tools  # List of synchronous tools
async_tools = toolkit.async_tools  # List of asynchronous tools
```

---

### Properties Provided by `BaseFunction`

The `BaseFunction` class includes several key properties that provide metadata and functionality for tools. These properties ensure compatibility with schemas (e.g., OpenAI tools) and facilitate interaction with wrapped functions.

#### 1. **`name`**
- **Description**: Retrieves the name of the wrapped function.
- **Source**: Extracted from the tool's schema.
- **Use Case**: Helpful for identifying the tool in toolkits, logs, or callbacks.

**Example:**
```python
print(my_tool.name)  # Outputs the tool's name from the schema
```

---

#### 2. **`description`**
- **Description**: Returns the tool's description, providing details about its purpose or functionality.
- **Source**: Pulled from the schema's `description` field.
- **Use Case**: Useful for documentation or dynamically presenting tool details to agents.

**Example:**
```python
print(my_tool.description)  # Outputs the tool's description
```

---

#### 3. **`parameters`**
- **Description**: Retrieves a dictionary of parameter definitions from the tool's schema.
- **Source**: Defined in the schema under `parameters.properties`.
- **Use Case**: Used for validation, introspection, or dynamically generating UI for tool invocation.

**Example:**
```python
print(my_tool.parameters)
# Outputs a dictionary of parameters, e.g., {"a": {"type": "integer"}, "b": {"type": "integer"}}
```

---

### Summary of Properties

| **Property**   | **Description**                                    | **Use Case**                              |
|-----------------|----------------------------------------------------|-------------------------------------------|
| `name`         | Name of the tool, extracted from the schema.       | Identification in logs, debugging, or UI. |
| `description`  | Description of the tool's purpose/functionality.   | Documentation or agent interaction.       |
| `parameters`   | Dictionary of parameter definitions for the tool.  | Validation, dynamic UI generation.        |

These properties make `BaseFunction` a powerful abstraction for managing tools, ensuring they are self-descriptive, schema-compliant, and easy to integrate into the Synthora framework.

---

### Toolkits Provided by Synthora

| **Toolkit Name**              | **Description**                                      | **Tools/Methods**                                                                                  |
|-------------------------------|------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| **BasicMathToolkit**          | Provides methods for basic math operations.          | `add`, `subtract`, `multiply`, `divide`                                                           |
| **FileToolkit**               | Handles file operations.                             | `read_file`, `write_file`, `delete_file`, `copy_file`, `move_file`, `search_file`, `list_directory`|
| **SlidesToolkit**             | A toolkit for creating slides.                       | *Custom slide creation tools (not detailed in the code)*                                           |
| **SearchToolkit**             | Enables various search functionalities.              | `search_wikipedia`, `search_google`, `search_arxiv`, `search_youtube`, `search_duckduckgo`         |
| **WeatherToolkit**            | Fetches weather data.                                | *Tools for weather fetching (not detailed in the code)*                                            |
| **TrafilaturaWebpageReader**  | Extracts main content from webpages using Trafilatura.| *General webpage reading tools based on Trafilatura*                                              |
| `get_webpage` | A  function to retrieve webpage text content using BeautifulSoup. | Accepts a URL and extracts the text content of the webpage.                                        |

This table highlights the modular structure of Synthora's toolkits, which provide specialized functionalities for different use cases, such as mathematical calculations, file operations, and content extraction.

---

### Summary of Key Properties and Methods

- **`@tool`**: Marks a function or method as a tool, initializing it as `SyncFunction` or `AsyncFunction`.
- **`BaseFunction.wrap()`**: Determines whether a function is sync or async and creates the appropriate wrapper.
- **Execution**:
  - `run`: Synchronous execution with callbacks.
  - `async_run`: Asynchronous execution with callbacks.
- **Toolkit Management**:
  - `BaseToolkit`: Automatically collects and organizes tools.

This structure ensures that tools in Synthora are well-integrated, extensible, and capable of handling complex workflows seamlessly.
