from synthora.messages import BaseMessage
from synthora.types.enums import MessageRole, NodeType
from synthora.types.node import Node


user_message = BaseMessage.create_message(
    role=MessageRole.USER,
    content="Hello, Synthora!",
    source=Node(name="user", type=NodeType.USER),
    metadata={"user_id": "1234"},
)

user_message_with_image = BaseMessage.create_message(
    role=MessageRole.USER,
    content="Hello, Synthora!",
    images=["https://example.com/image.jpg"],
    source=Node(name="user", type=NodeType.USER),
    metadata={"user_id": "1234"},
)

function_response_message = BaseMessage.create_message(
    id="1234",
    role=MessageRole.TOOL_RESPONSE,
    content="Hello, Synthora!",
    source=Node(name="function", type=NodeType.TOOLKIT),
    metadata={"tool_call_id": "1234"},
)
retriever_message = BaseMessage.create_message(
    role=MessageRole.RETRIEVER,
    content="Hello, Synthora!",
    source=Node(name="retriever", type=NodeType.RETRIEVER),
    metadata={"retriever_id": "1234"},
)
retriever_message_with_image = BaseMessage.create_message(
    role=MessageRole.RETRIEVER,
    content="Hello, Synthora!",
    images=["https://example.com/image.jpg"],
    source=Node(name="retriever", type=NodeType.RETRIEVER),
    metadata={"retriever_id": "1234"},
)

assistant_message = BaseMessage.create_message(
    role=MessageRole.ASSISTANT,
    content="Hello, Synthora!",
    source=Node(name="assistant", type=NodeType.AGENT),
    metadata={"assistant_id": "1234"},
)


print(user_message.to_openai_message())
print(user_message_with_image.to_openai_message())
print(function_response_message.to_openai_message())
print(retriever_message.to_openai_message())
print(retriever_message_with_image.to_openai_message())
print(assistant_message.to_openai_message())
