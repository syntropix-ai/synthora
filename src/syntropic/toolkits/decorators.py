import inspect
from typing import Any, Callable, Union
from syntropic.toolkits.base import BaseFunction


def tool(
    func: Callable[..., Any]
) -> Union[BaseFunction, Callable[..., Any]]:
    signature = inspect.signature(func)
    parameters = list(signature.parameters.values())
    if parameters and parameters[0].name == "self":
        setattr(func, "_flag", True)
        return func
    return BaseFunction.wrap(func)
