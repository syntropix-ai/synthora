from typing import Any, Optional, Union, TYPE_CHECKING
from synthora.types.enums import TaskState
from synthora.workflows.base_task import BaseTask
from synthora.workflows.context.base import BaseContext
if TYPE_CHECKING:
    from synthora.workflows.scheduler.base import BaseScheduler


class BasicContext(dict, BaseContext):
    def __init__(self, workflow: "BaseScheduler") -> None:
        super().__init__()
        self._workflow = workflow
        

    @property
    def lock(self) -> None:
        pass
    
    def acquire(self) -> None:
        pass
    
    def release(self) -> None:
        pass
        
    def get_task(self, name: str) -> Optional[Union["BaseScheduler", BaseTask]]:
        return self._workflow.get_task(name)
    
    def end(self) -> None:
        self._workflow.state = TaskState.COMPLETED
    
    def skip(self, name: str) -> None:
        self.get_task(name).state = TaskState.SKIPPED
    
        
    def get_state(self, name: str) -> TaskState:
        if task := self.get_task(name):
            return task.state
        raise KeyError(f"Task {name} not found")
    
    def set_state(self, name: str, state: TaskState) -> None:
        if task := self.get_task(name):
            task.state = state
        else:
            raise KeyError(f"Task {name} not found")
    
    def get_result(self, name: str) -> Any:
        if task := self.get_task(name):
            return task.result()
        raise KeyError(f"Task {name} not found")
    
    def set_result(self, name: str, result: Any) -> None:
        if task := self.get_task(name):
            task._result = result
        else:
            raise KeyError(f"Task {name} not found")
        
    @property
    def workflow(self) -> "BaseScheduler":
        return self._workflow
    
    
    
    
    
    
    
        
    
