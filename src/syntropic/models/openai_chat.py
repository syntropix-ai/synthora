from typing import Any, Dict, Optional
from syntropic.models import BaseModelBackend
from openai import OpenAI
import os
from openai import types


class OpenAIChatBackend(BaseModelBackend):
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs: Dict[str, Any]) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.kwargs = kwargs
        self.config = config or {}
        self.kwargs["api_key"] = self.api_key
        self.kwargs["base_url"] = self.base_url

        self.client = OpenAI(**self.kwargs)

        super().__init__()

    def run(self, **kwargs: Dict[str, Any]) -> Any:
        return self.client.chat.completions.create(**kwargs)

    async def async_run(self, **kwargs: Dict[str, Any]) -> Any:
        return self.client.chat.conversations.create(**kwargs)
