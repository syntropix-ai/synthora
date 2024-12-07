from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Union

from synthora.agents.base import BaseAgent
from synthora.models.base import BaseModelBackend
from synthora.toolkits.base import BaseFunction

ItemType = Union[BaseAgent, BaseFunction, BaseModelBackend]


class BaseExecutor(ABC):
    def __init__(self, can_be_root: bool) -> None:
        self.can_be_root = can_be_root

    @abstractmethod
    def wrap(
        self, items: Union[ItemType, List[ItemType]]
    ) -> Union[ItemType, List[ItemType]]: ...

    @abstractmethod
    def submit(self, func: Callable, *args: Any, **kwargs: Dict[str, Any]): ...
    
    @abstractmethod
    def run(self):...
