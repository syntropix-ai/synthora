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

# Message


## Overview

`BaseMessage` is a core class designed to manage and structure different types of chat messages in conversational AI systems. It supports user interactions, system announcements, assistant responses, and tool-based operations. The class provides a robust framework for validating, processing, and integrating messages within an AI-driven architecture.

---

## **Key Features**

- **Content Validation**: Ensures all messages are well-formed and meaningful, preventing incomplete or empty messages.
- **Role Management**: Differentiates the roles of message senders, including user, system, assistant, and tool-related interactions.
- **Tool Interaction Handling**: Supports the inclusion of tool calls and tool responses as part of the message.
- **Integration-Ready**: Provides seamless conversion of messages to formats compatible with APIs like OpenAI.
- **Metadata Support**: Allows storage of additional contextual information related to each message.

---

## **Class Breakdown**

The `BaseMessage` class is defined as follows:

```python
class BaseMessage(BaseModel):
    """Base message class for handling different types of chat messages.

    Attributes:
        id:
            A unique identifier for the message.
        source:
            The source node that originated the message.
        role:
            The role of the message sender (e.g., user, assistant, system, tool).
        chunk:
            A partial chunk of streamed message content.
        parsed:
            Parsed content of the message, useful for preprocessed data.
        content:
            The main textual content of the message.
        tool_calls:
            A list of tool calls initiated by the message.
        tool_response:
            The response received from any tool execution.
        images:
            A list of image URLs associated with the message.
        origional_response:
            The original response data from OpenAI or similar systems.
        metadata:
            A dictionary to store additional metadata or context for the message.
    """

    id: Optional[str] = None
    source: Node
    role: MessageRole

    chunk: Optional[str] = None
    parsed: Optional[Any] = None
    content: Optional[str] = None
    tool_calls: Optional[List[ChatCompletionMessageToolCall]] = None
    tool_response: Optional[Dict[str, Any]] = None
    images: Optional[List[str]] = None
    origional_response: Optional[
        Union[ChatCompletion, ChatCompletionChunk]
    ] = None

    metadata: Dict[str, Any] = {}
```

---

## **Key Properties and Behaviors**

### **Attributes**

- **`id`**: A unique identifier for each message, useful for tracking.
- **`source`**: The origin of the message, represented by a `Node` object.
- **`role`**: The role of the message sender, such as user, assistant, system, or tool.
- **`chunk`**: Supports streamed content by representing a portion of the message.
- **`parsed`**: Parsed content for cases where the message undergoes preprocessing or analysis.
- **`content`**: The main text content of the message.
- **`tool_calls`**: A list of tool calls initiated by the message, enabling interaction with external systems or APIs.
- **`tool_response`**: A dictionary containing the response from any executed tools.
- **`images`**: A list of image URLs related to the message.
- **`origional_response`**: Stores the original response object from systems like OpenAI.
- **`metadata`**: A dictionary for storing extra contextual information.

### **Validation**

The `BaseMessage` class enforces strict validation:
- At least one of the following attributes must be populated: `content`, `images`, `tool_calls`, or `tool_response`.

---

## **Creating Messages**

The `BaseMessage` class provides flexibility for creating various types of messages. Here are some examples:

### **1. User Message**

To create a user message:

```python
from synthora.types.node import Node
from synthora.types.enums import MessageRole, NodeType
from synthora.messages import BaseMessage

message = BaseMessage(
    role=MessageRole.USER,
    content="Hello, World!",
    source=Node(name="user", type=NodeType.USER)
)
```

### **2. System Message**

To create a system-generated message:

```python
message = BaseMessage(
    role=MessageRole.SYSTEM,
    content="System initialized successfully."
)
```

### **3. Assistant Message**

To create a response from the assistant:

```python
message = BaseMessage(
    role=MessageRole.ASSISTANT,
    content="How can I assist you today?"
)
```

### **4. Tool-Response Message**

To define interactions with a tool, including the tool's response:

```python
message = BaseMessage(
    role=MessageRole.TOOL_RESPONSE,
    content="Here is the data you requested.",
    tool_response={"result": "success"}
)
```

---

## **Integration with OpenAI**

The `BaseMessage` class supports integration with OpenAI’s API by providing conversion utilities.

### **Converting to OpenAI-Compatible Format**

To convert a `BaseMessage` instance into a format compatible with OpenAI:

```python
openai_message = message.to_openai_message()
```

### **Processing OpenAI Responses**

To process responses from OpenAI into a `BaseMessage` object:

```python
from_openai_message = BaseMessage.from_openai_chat_response(response)
```

---

## **Helper Methods**

To streamline the creation of common message types, several utility methods are provided:

- **`user(content)`**: Quickly create a user message.
- **`system(content)`**: Quickly create a system message.
- **`assistant(content, name="assistant")`**: Quickly create an assistant message.

### **Examples**

```python
from synthora.messages import user, system, assistant

user_message = user("Hi there!")
system_message = system("Welcome to the system.")
assistant_message = assistant("Hello! I’m here to help.")
```

---

## **Best Practices**

1. **Use Metadata**: Utilize the `metadata` attribute to store additional contextual details about messages.
2. **Validation**: Always ensure messages meet the validation rules to avoid runtime errors.
3. **Streamed Content**: Leverage the `chunk` attribute for handling partial content in streamed responses.
4. **Tool Interaction**: Utilize `tool_calls` and `tool_response` attributes for implementing interactive capabilities.

---

## **Conclusion**

The `BaseMessage` class is a powerful and flexible tool for managing chat messages in conversational AI systems. Its robust design ensures smooth integration with APIs, support for complex interactions, and scalability for future enhancements. By leveraging its features, developers can build efficient, interactive, and context-aware chat systems.
