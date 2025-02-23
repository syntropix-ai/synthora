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
import re
from copy import deepcopy
from typing import Any, Callable, Dict, Optional, Union


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from synthora.agents.base import BaseAgent
from synthora.memories.summary_memory import SummaryMemory
from synthora.models.base import BaseModelBackend
from synthora.services.base import BaseService
from synthora.toolkits.base import BaseFunction
from synthora.workflows.base_task import BaseTask
from synthora.workflows.scheduler.base import BaseScheduler


class SlackBotService(BaseService):
    def __init__(
        self, bot_token: Optional[str] = None, app_token: Optional[str] = None
    ) -> None:
        self.bot_token = bot_token or os.environ.get("SLACK_BOT_TOKEN", None)
        if not self.bot_token:
            raise ValueError(
                "SLACK_BOT_TOKEN is required to run the SlackBotService."
            )
        self.app_token = app_token or os.environ.get("SLACK_APP_TOKEN", None)
        if not self.app_token:
            raise ValueError(
                "SLACK_APP_TOKEN is required to run the SlackBotService."
            )
        self.app = App(token=self.bot_token)
        self.agent_map: Dict[str, BaseAgent] = {}
        super().__init__()

    def add(
        self,
        target: Union[
            BaseAgent, BaseModelBackend, BaseFunction, BaseTask, BaseScheduler
        ],
        name: Optional[str] = None,
    ) -> Self:
        if len(self.service_map) > 0:
            raise ValueError(
                "SlackBotService can only have one target. You can add "
                "multiple services manually."
            )
        if isinstance(target, BaseAgent):
            name = name or target.name
            if isinstance(target.model, BaseModelBackend):
                target.model.client = None
            else:
                for model in target.model:
                    model.client = None
            if isinstance(target.history, SummaryMemory):
                target.history.summary_model.client = None

            def _target(
                event: Dict[str, Any], say: Callable[..., Any]
            ) -> None:
                user = event["user"]
                text = event["text"]
                channel = event["channel"]

                text = re.sub(r"<@.*?>", "", text, count=1)
                print(f"{user} said: {text} in channel {channel}")
                if user not in self.agent_map:
                    self.agent_map[user] = deepcopy(target)

                prompt = f"{user} said: {text} in channel {channel}"
                resp = self.agent_map[user].run(prompt)

                if resp.is_ok:
                    say(
                        blocks=[
                            {
                                "type": "context",
                                "elements": [{"type": "mrkdwn", "text": text}],
                            },
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": resp.unwrap().content,
                                },
                            },
                        ]
                    )
                else:
                    say(f"An error occurred: {resp.unwrap_err_val()}")

            self.service_map[str(name)] = target
            self.app.event("app_mention")(_target)
        return self

    def run(self, *args: Any, **kwargs: Any) -> Self:
        if "app_token" not in kwargs:
            kwargs["app_token"] = self.app_token
        SocketModeHandler(self.app, *args, **kwargs).start()
        return self

    def stop(self) -> Self:
        return self
