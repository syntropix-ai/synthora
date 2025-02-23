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

## 🛠️ What is `BaseMessage`?

`BaseMessage` is a foundational class that helps manage various types of chat messages—user messages, system messages, assistant responses, and even tool interactions. Think of it as your ultimate message toolkit.

### Key Features:
- **Content Validation**: Ensures messages are well-formed and meaningful.
- **Role Management**: Differentiates between users, systems, and assistants.
- **Integration-Friendly**: Converts messages to formats compatible with OpenAI or similar APIs.
- **Tool Interactions**: Handles tool calls and responses effortlessly.



## 📦 Class Breakdown

Here’s an overview of the class and its attributes:

```python
class BaseMessage(BaseModel):
    """Base message class for handling different types of chat messages."""

    id: Optional[str] = None  # Unique identifier for the message
    source: Node             # Source of the message (e.g., user, assistant)
    role: MessageRole        # Who's talking? (User, System, Assistant, Tool)
    chunk: Optional[str] = None
    content: Optional[str] = None
    tool_calls: Optional[List[ChatCompletionMessageToolCall]] = None
    tool_response: Optional[Dict[str, Any]] = None
    images: Optional[List[str]] = None
    metadata: Dict[str, Any] = {}  # Extra details
```

### 🚀 Cool Properties:

1. **`is_complete`**: Check if the message is done and dusted.
2. **`has_tool_calls`**: Does the message involve any tools? Let’s find out!
3. **Validation**: Messages need at least one of `content`, `images`, `tool_calls`, or `tool_response`. No empty shells here.



## 🌟 Let’s Build Some Messages!

### 1. **User Message**
Want to simulate a user saying “Hello, World”? Easy!

```python
from synthora.types.node import Node
from synthora.types.enums import MessageRole, NodeType
from synthora.messages import BaseMessage

message = BaseMessage.create_message(
    role=MessageRole.USER,
    content="Hello, World!",
    source=Node(name="user", type=NodeType.USER)
)
```

### 2. **System Message**
For backend or system announcements, use:

```python
message = BaseMessage.create_message(
    role=MessageRole.SYSTEM,
    content="System initialized successfully."
)
```

### 3. **Assistant Message**
Here’s how your chatbot can reply like a pro:

```python
message = BaseMessage.create_message(
    role=MessageRole.ASSISTANT,
    content="How can I assist you today?"
)
```

### 4. **Tool-Response Message**
If the assistant’s using tools, define those interactions:

```python
message = BaseMessage.create_message(
    role=MessageRole.TOOL_RESPONSE,
    content="Here’s the data you requested.",
    tool_response={"result": "success"}
)
```



## 🌐 OpenAI Integration

Need OpenAI-compatible messages? We’ve got you covered! Simply convert your `BaseMessage`:

```python
openai_message = message.to_openai_message()
```

You can even process streaming responses seamlessly:

```python
from_openai_message = BaseMessage.from_openai_chat_response(response)
```



## 🌟 Bonus Helpers

We’ve included utility methods for your convenience:

- **`user(content)`**: Quick-create a user message.
- **`system(content)`**: Snap a system message into place.
- **`assistant(content, name="assistant")`**: Build your assistant's personality.

Example:

```python
from synthora.messages import user, system, assistant

user_message = user("Hi there!")
system_message = system("Welcome to the system.")
assistant_message = assistant("Hello! I’m here to help.")
```



## 💡 Tips & Tricks

- Use `metadata` to store extra details about messages.
- Always validate your messages to avoid runtime errors.
- Explore the `tool_calls` feature for interactive assistant capabilities.



Thanks for exploring `BaseMessage` with us! Happy coding! 🎉
