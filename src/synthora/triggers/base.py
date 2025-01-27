from abc import ABC, abstractmethod
from typing import Dict, Self, Union

from synthora.agents.base import BaseAgent
from synthora.toolkits.base import BaseFunction
from synthora.types.enums import TriggerRuntime


class BaseTrigger(ABC):

    def __init__(self, args_name: str) -> None:
        self.args_name = args_name

    @abstractmethod
    def add(
        self, obj: Union[BaseFunction, BaseAgent]
    ) -> Self: ...
