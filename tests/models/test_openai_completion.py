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

from synthora.messages import user
from synthora.messages.base import BaseMessage
from synthora.models.openai_completion import OpenAICompletionBackend


@pytest.fixture(scope="class")
def openai_completion_model() -> OpenAICompletionBackend:
    return OpenAICompletionBackend.default(
        model_type="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    )


@pytest.fixture(scope="class")
def openai_completion_model_stream() -> OpenAICompletionBackend:
    return OpenAICompletionBackend.default(
        model_type="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        config={"stream": True},
    )


@pytest.mark.requires_env("OPENAI_API_KEY")
class TestOpenAICompletion:
    def test_openai_completion(
        self, openai_completion_model: OpenAICompletionBackend
    ):
        message = user(content="Say 'Hello, World!' in French")
        response = openai_completion_model.run(message)

        assert isinstance(response, BaseMessage)
        assert response.content is not None
        assert len(response.content) > 0
        assert "bonjour" in response.content.lower()

    def test_openai_completion_stream(
        self, openai_completion_model_stream: OpenAICompletionBackend
    ):
        message = user(content="Say 'Hello, World!' in French")
        stream = openai_completion_model_stream.run(message)

        chunks = []
        for chunk in stream:
            assert isinstance(chunk, BaseMessage)
            chunks.append(chunk)

        final_content = "".join(
            chunk.content for chunk in chunks if chunk.content
        )
        assert len(final_content) > 0
        assert "bonjour" in final_content.lower()

    async def test_openai_completion_async(
        self, openai_completion_model: OpenAICompletionBackend
    ):
        message = user(content="Say 'Hello, World!' in French")
        response = await openai_completion_model.async_run(message)

        assert isinstance(response, BaseMessage)
        assert len(response.content) > 0
        assert "bonjour" in response.content.lower()

    async def test_openai_completion_async_stream(
        self, openai_completion_model_stream: OpenAICompletionBackend
    ):
        message = user(content="Say 'Hello, World!' in French")
        stream = await openai_completion_model_stream.async_run(message)

        chunks = []
        async for chunk in stream:
            assert isinstance(chunk, BaseMessage)
            chunks.append(chunk)

        final_content = "".join(
            chunk.content for chunk in chunks if chunk.content
        )
        assert len(final_content) > 0
        assert "bonjour" in final_content.lower()
