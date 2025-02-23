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

# Memory

This document provides an overview of the memory-related classes defined in the provided code snippet, along with the scenarios where each type of memory is most suitable. These classes are designed to manage and process message histories efficiently in different contexts.

---

## **Base Classes**

### **BaseMessage**
`BaseMessage` represents individual messages exchanged in the system. It serves as the foundation for all memory management operations.

---

### **BaseMemory**
`BaseMemory` is an abstract base class (ABC) that provides the structure for memory management. It requires subclasses to implement an asynchronous method (`async_append`) for adding messages.

---

## **Memory Implementations**

### **1. FullContextMemory**

#### **Overview:**
`FullContextMemory` stores the entire conversation history in a sequential manner without any truncation or removal of messages. It is a straightforward implementation of `BaseMemory` and retains all messages indefinitely.

#### **Use Case:**
- Best suited for scenarios where **complete conversation history** needs to be preserved without loss of information.
- Ideal for applications like **log keeping**, **debugging**, or **auditing**, where every message must be retained for future reference.

---

### **2. RecentNMemory**

#### **Overview:**
`RecentNMemory` retains only the most recent `n` messages while discarding older ones, except for system messages. It ensures that memory usage is capped, making it efficient for scenarios where storage or processing needs to be optimized.

#### **Use Case:**
- Suitable for **real-time applications** where only the latest context is relevant, such as:
  - Chatbots with limited memory capacity.
  - Systems handling **short-lived tasks**, where older conversations are irrelevant.
  - Applications requiring **memory efficiency** in resource-constrained environments.

#### **How It Works:**
- Messages beyond the limit (`n`) are removed dynamically.
- System messages (`MessageRole.SYSTEM`) are preserved to maintain important system instructions or context.

---

### **3. SummaryMemory**

#### **Overview:**
`SummaryMemory` extends `BaseMemory` by summarizing conversation histories after they exceed a specified limit (`n`). It uses an AI model (default: `OpenAIChatBackend`) to generate concise summaries, replacing multiple messages with a single summary for efficient storage.

#### **Use Case:**
- Suitable for **long-term memory management** where retaining the entire history is impractical but summarizing key points is essential. Examples include:
  - **Conversational agents** that need to maintain context over long interactions.
  - **Knowledge base updates**, where the system summarizes discussions for easier reference.
  - **Complex workflows**, where concise summaries are required to track progress without storing every detail.

#### **How It Works:**
- When the number of messages exceeds the limit (`n`), it selects recent messages (up to `cache_size`) for summarization.
- Summaries are generated in the **third person** to maintain an objective tone.
- After summarization, summarized messages are replaced with the summary.

---

## **Comparison of Memory Types**

| **Memory Type**       | **Preserves Entire History** | **Truncates Old Messages** | **Summarizes Messages** | **Best For**                                                                 |
|------------------------|-----------------------------|----------------------------|--------------------------|------------------------------------------------------------------------------|
| FullContextMemory      | Yes                         | No                         | No                       | Applications requiring complete logs or full conversation tracking.         |
| RecentNMemory          | No                          | Yes                        | No                       | Real-time or short-lived tasks where only recent context matters.           |
| SummaryMemory          | No                          | Yes (via summarization)    | Yes                      | Long-term memory with concise summaries for maintaining key context.        |

---

## **Examples of Usage Scenarios**

### **1. FullContextMemory**
- **Scenario:** A debugging tool that records all user interactions with a system for auditing purposes.
- **Code Example:**
  ```python
  memory = FullContextMemory()
  message = BaseMessage(content="Debug this issue.", role=MessageRole.USER)
  memory.append(message)
  # OR
  await memory.async_append(message)
  ```

### **2. RecentNMemory**
- **Scenario:** A chatbot handling short, real-time conversations where only the last 10 messages are needed.
- **Code Example:**
  ```python
  memory = RecentNMemory(n=10)
  message = BaseMessage(content="Hello, chatbot!", role=MessageRole.USER)
  memory.append(message)
  # OR
  memory.append(message)
  ```

### **3. SummaryMemory**
- **Scenario:** A virtual assistant summarizing long conversations into actionable insights for a user.
- **Code Example:**
  ```python
  memory = SummaryMemory(n=15, cache_size=6)
  message = BaseMessage(content="Explain the project details.", role=MessageRole.USER)
  memory.append(message)
  # OR
  await memory.async_append(message)  # Triggers summarization if limit is exceeded.
  ```

---

## **Key Benefits**
- **FullContextMemory:** Ensures no loss of information.
- **RecentNMemory:** Optimized for performance with limited memory usage.
- **SummaryMemory:** Balances memory efficiency with the need to retain essential context through summarization.

This documentation explains the purpose and suitability of each memory type, enabling users to choose the right class based on their specific application requirements.
