import os
from typing import Any, Dict, Optional, Self, Union
from synthora.agents.base import BaseAgent
from synthora.models.base import BaseModelBackend
from synthora.services.base import BaseService
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from synthora.toolkits.base import BaseFunction
from synthora.workflows.base_task import BaseTask
from synthora.workflows.scheduler.base import BaseScheduler

class SlackBotService(BaseService):
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or os.environ.get("SLACK_API_KEY", None)
        if not self.api_key:
            raise ValueError("API key is required to run the SlackBotService.")
        self.app = App(token=self.api_key)
        super().__init__()

    def add(self, target: Union[BaseFunction, BaseAgent, BaseModelBackend, BaseTask, BaseScheduler], name: Optional[str] = None) -> Self:
        if isinstance(target, BaseAgent):
            self.service_map[name or target.name] = target
        return self

    def run(self, *args: Any, **kwargs: Dict[str, Any]) -> Self:
        if 'app_token' not in kwargs:
            kwargs['app_token'] = self.api_key
        SocketModeHandler(self.app, *args, **kwargs).start()
        return self

    def stop(self) -> Self:
        return self
