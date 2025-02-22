# LICENSE HEADER MANAGED BY add-license-header
#
# Copyright 2024-2025 Syntropix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

import pytest

from synthora.messages import system, user
from synthora.messages.base import BaseMessage
from synthora.models.openai_chat import OpenAIChatBackend


@pytest.fixture(scope="class")
def openai_chat_model() -> OpenAIChatBackend:
    return OpenAIChatBackend.default(
        model_type="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    )


@pytest.fixture(scope="class")
def openai_chat_model_stream() -> OpenAIChatBackend:
    return OpenAIChatBackend.default(
        model_type="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        config={"stream": True},
    )


@pytest.mark.requires_env("OPENAI_API_KEY")
class TestOpenAIChat:
    def test_openai_chat(self, openai_chat_model: OpenAIChatBackend):
        # Test basic chat completion
        message = user(content="Say 'Hello, World!' in French")
        response = openai_chat_model.run(message)

        assert isinstance(response, BaseMessage)
        assert response.content is not None
        assert len(response.content) > 0
        assert "Bonjour" in response.content or "bonjour" in response.content

    def test_openai_chat_stream(
        self, openai_chat_model_stream: OpenAIChatBackend
    ):
        # Test streaming chat completion
        message = user(content="Count from 1 to 5")
        stream = openai_chat_model_stream.run(message)

        chunks = []
        for chunk in stream:
            assert isinstance(chunk, BaseMessage)
            chunks.append(chunk)

        # Combine all chunks
        final_content = "".join(
            chunk.content for chunk in chunks if chunk.content
        )
        assert any(str(i) in final_content for i in range(1, 6))

    async def test_openai_chat_async(
        self, openai_chat_model: OpenAIChatBackend
    ):
        # Test async chat completion
        message = user(content="What is 2+2?")
        response = await openai_chat_model.async_run(message)

        assert isinstance(response, BaseMessage)
        assert response.content is not None
        assert "4" in response.content

    async def test_openai_chat_async_stream(
        self, openai_chat_model_stream: OpenAIChatBackend
    ):
        # Test async streaming chat completion
        message = user(content="Name three colors")
        stream = await openai_chat_model_stream.async_run(message)

        chunks = []
        async for chunk in stream:
            assert isinstance(chunk, BaseMessage)
            chunks.append(chunk)

        # Combine all chunks
        final_content = "".join(
            chunk.content for chunk in chunks if chunk.content
        )
        assert len(final_content) > 0
        # Common colors that might appear in the response
        common_colors = ["red", "blue", "green", "yellow", "black", "white"]
        assert any(color in final_content.lower() for color in common_colors)

    def test_openai_chat_with_system_message(
        self, openai_chat_model: OpenAIChatBackend
    ):
        # Test chat completion with system message
        system_msg = system(
            content="You are a pirate who speaks in pirate language.",
        )
        user_msg = user(content="Say hello and introduce yourself")

        response = openai_chat_model.run([system_msg, user_msg])

        assert isinstance(response, BaseMessage)
        assert response.content is not None
        # Look for common pirate terms
        pirate_terms = ["arr", "matey", "ahoy", "ye", "captain"]
        assert any(term in response.content.lower() for term in pirate_terms)
