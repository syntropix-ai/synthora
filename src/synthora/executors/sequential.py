from typing import Any, Callable, Dict, List, Union
from synthora.executors.base import BaseExecutor, ItemType


class SequentialExecutor(BaseExecutor):
    def __init__(self):
        super().__init__(True)

    def wrap(
        self, items: Union[ItemType, List[ItemType]]
    ) -> Union[ItemType, List[ItemType]]:
        return items

    def submit(self, func: Callable, *args: Any, **kwargs: Dict[str, Any]): 
        pass
