from abc import ABC, abstractmethod
from typing import Callable, Dict, Optional, Self, Union

from synthora.agents.base import BaseAgent
from synthora.models.base import BaseModelBackend


class BaseService(ABC):
    def __init__(self) -> None:
        self.service_map: Dict[str, Union[Callable, BaseAgent, BaseModelBackend]] = {}

    @abstractmethod
    def add(self, target: Union[Callable, BaseAgent, BaseModelBackend], name: Optional[str] = None) -> Self: ...

    @abstractmethod
    def run(self, *args, **kwargs) -> Self: ...
    
    @abstractmethod
    def stop(self) -> Self: ...
