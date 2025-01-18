# LICENSE HEADER MANAGED BY add-license-header
#
# Copyright 2024-2025 Syntropix-AI.org
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

import asyncio
import os
from typing import Optional, Self, Union

import discord

from synthora.agents.base import BaseAgent
from synthora.models.base import BaseModelBackend
from synthora.services.base import BaseService
from synthora.toolkits.base import BaseFunction
from synthora.workflows.base_task import BaseTask
from synthora.workflows.scheduler.base import BaseScheduler


class DiscordBotService(BaseService):
    def __init__(self, token: Optional[str] = None) -> None:
        token = token or os.environ.get("DISCORD_TOKEN")
        if not token:
            raise ValueError(
                "DISCORD_TOKEN is required to run the DiscordBotService."
            )
        self._token: str = token
        self._client = discord.Client(intents=discord.Intents.default())
        self._agent: Optional[BaseAgent] = None

        @self._client.event
        async def on_ready() -> None:
            print(f"Logged in as {self._client.user}")

        @self._client.event
        async def on_message(message: discord.Message) -> None:
            username = message.author.global_name
            userid = message.author.id
            user_message = str(message.content)

            if message.author == self._client.user:
                return

            if not user_message:
                return

            if not self._agent:
                await message.channel.send("Error: No Backend Agent Set")
                return

            print(f"{username} ({userid}) said: {user_message}")

            user_msg_prompt = f"{username} ({userid}) said: {user_message}"
            response = await self._agent.async_run(user_msg_prompt)

            text_response = response.unwrap().content
            try:
                await message.channel.send(text_response)
            except Exception:
                await message.channel.send("An error occurred.")

        super().__init__()

    def add(
        self,
        agent: Union[
            BaseAgent, BaseModelBackend, BaseFunction, BaseTask, BaseScheduler
        ],
        name: Optional[str] = None,
    ) -> Self:
        if not isinstance(agent, BaseAgent):
            raise NotImplementedError("Only BaseAgent is supported for now")
        self._agent = agent
        return self

    def run(self) -> Self:
        asyncio.run(self._client.start(self._token))
        return self

    def stop(self) -> Self:
        asyncio.run(self._client.close())
        return self
