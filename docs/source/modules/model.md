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

# ModelBackend
## Overview

The `BaseModelBackend` class is an abstract interface for creating various model backend implementations. It defines core functionalities like initialization, synchronous and asynchronous execution, and configuration handling. Subclasses, such as `OpenAIChatBackend` and `OpenAICompletionBackend`, implement the specific logic for different model providers or APIs.

---

## Key Methods

### 1. **`default` Method**
The `default` method is a static factory method that creates a default instance of a specific backend implementation. It simplifies initialization by providing default values while allowing customization through parameters.

#### **Parameters**:
- **`model_type`**: The type or identifier of the model (e.g., `'gpt-4'`).
- **`source`**: A `Node` instance representing the model's context or origin.
- **`config`**: A dictionary of configuration parameters for fine-tuning the backend.
- **`name`**: An optional name for the backend instance.
- **`handlers`**: A list of callback handlers (`BaseCallBackHandler` or `AsyncCallBackHandler`) for managing events during model execution.

#### **Example**:
Using `OpenAIChatBackend`:
```python
from synthora.types.node import Node
from synthora.types.enums import ModelBackendType

# Create a source node
source_node = Node(name="assistant", type=NodeType.AGENT)

# Initialize the backend using default
chat_backend = OpenAIChatBackend.default(
    model_type="gpt-4",
    source=source_node,
    config={"temperature": 0.8, "max_tokens": 1000},
    name="ChatBackend",
    handlers=[]
)
```

---

### 2. **`run` Method**
The `run` method is an abstract method designed for synchronous execution of the model. Subclasses implement this method to handle input messages and return model outputs.

#### **Parameters**:
- **`messages`**: A single message or a list of `BaseMessage` instances representing the input.
- **`*args` and `**kwargs`**: Additional arguments and keyword arguments for execution.

#### **Example**:
Using `OpenAIChatBackend`:
```python
from synthora.messages import user

# Prepare input messages
messages = [user(content="Hello, how are you?")]

# Run the backend synchronously
response = chat_backend.run(messages)
print(response)
```

---

### 3. **`async_run` Method**
The `async_run` method provides asynchronous execution of the model. This is useful for handling large-scale or time-sensitive tasks without blocking the main application.

#### **Parameters**:
- **`messages`**: A single message or a list of `BaseMessage` instances as input.
- **`*args` and `**kwargs`**: Additional arguments and keyword arguments for execution.

#### **Example**:
Using `OpenAIChatBackend`:
```python
import asyncio
from synthora.messages import user

# Prepare input messages
messages = [user(content="What's the weather today?")]

# Asynchronously execute the model
async def get_response():
    response = await chat_backend.async_run(messages)
    print(response)

asyncio.run(get_response())
```

---

### 4. **`stream` Property**
The `stream` property indicates whether the backend is configured to use streaming output. Streaming is useful for real-time applications, such as live text generation.

#### **Usage**:
- To check the streaming status:
```python
is_streaming = chat_backend.stream
print(f"Streaming enabled: {is_streaming}")
```

- To enable or disable streaming:
```python
chat_backend.set_stream(True)
print("Streaming enabled.")
```

---

## Supported Backends

### 1. **`OpenAIChatBackend`**
The `OpenAIChatBackend` subclass is specifically designed to support OpenAI's chat-based models, such as `gpt-4` and `gpt-3.5-turbo`. These models are optimized for conversational AI tasks and provide excellent capabilities for a wide range of chat-oriented applications.

**Key Features**:
- **Support for OpenAI Models**: Tailored to handle chat-based interactions using OpenAI's API format.
- **Flexible Configuration**: Allows customization of parameters such as API key, base URL, temperature, and token limits to suit specific application needs.
- **Callback Integration**: Compatible with both synchronous and asynchronous callback handlers to enable real-time event processing during model execution.

### 2. **`OpenAICompletionBackend`**
The `OpenAICompletionBackend` subclass extends the `OpenAIChatBackend` to handle OpenAI's completion models. While it shares most features with `OpenAIChatBackend`, this backend is focused on tasks that require free-form text generation or structured completions, rather than conversational exchanges.

**Key Features**:
- **Completion-Oriented Design**: Geared toward non-conversational tasks such as text summarization, classification, and general text generation.
- **Inherited Features**: Supports the same configuration options and callback integration mechanisms as the `OpenAIChatBackend`.

---

### Why Synthora Currently Supports OpenAI Formats

Currently, Synthora supports the OpenAI API format for both chat and completion backends. This choice is driven by practical considerations and industry trends:

1. **Compatibility with Local Deployment Frameworks**:
   Many popular local deployment frameworks, such as **vLLM**, provide OpenAI-compatible servers. By supporting the OpenAI API format, Synthora ensures compatibility with these frameworks, enabling users to integrate local models seamlessly while benefiting from OpenAI's standardized interface.

2. **Wide Adoption**:
   OpenAI's API format has become a de facto standard for interacting with language models. Supporting this format allows Synthora to cater to a broad spectrum of use cases without requiring custom integrations for each backend.

3. **Extensibility**:
   Although Synthora currently focuses on OpenAI compatibility, it is designed to be extensible. Adding support for other backend formats is possible, and we are open to contributions or requests for additional integrations in the future.

By leveraging the OpenAI-compatible ecosystem, Synthora meets the needs of most users while maintaining flexibility for future enhancements.

---

## Summary

The `BaseModelBackend` class and its subclasses provide a robust and extensible framework for integrating various model APIs. By defining common methods like `default`, `run`, `async_run`, and `stream`, it ensures a consistent interface while allowing custom implementations to tailor the functionality for specific use cases.
