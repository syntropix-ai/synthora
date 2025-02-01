from synthora.workflows.base_task import BaseTask
from synthora.workflows.context.base import BaseContext
from typing import Any, Callable
from synthora.workflows import task


def if_else(condition_func: Callable[..., bool], name_true: str, name_false: str) -> BaseTask:
    @task(flat_result=True)
    def _condition(context: BaseContext, *args: Any, **kwargs: Any) -> None:
        result = condition_func(context, *args, **kwargs)
        if result:
            context.skip(name_false)
        else:
            context.skip(name_true)
        if kwargs:
            return *args, kwargs
        return args
            
    return _condition
