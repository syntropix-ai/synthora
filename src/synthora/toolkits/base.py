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
# limitations under the License.

import asyncio
import inspect
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional, Union, cast

from synthora.callbacks.base_handler import BaseCallBackHandler
from synthora.callbacks.base_manager import (
    AsyncCallBackManager,
    BaseCallBackManager,
)
from synthora.types import Err, Ok, Result
from synthora.types.enums import CallBackEvent, NodeType
from synthora.types.node import Node
from synthora.utils import get_openai_tool_schema
from synthora.utils.macros import CALL_ASYNC_CALLBACK


class BaseFunction(ABC):
    """Abstract base class for function wrappers that can be used as tools.

    Provides common functionality for both synchronous and asynchronous
    function handling, including callback management and OpenAI tool schema
    generation.

    Attributes:
        instance: The class instance that owns this function (if method).
        func: The wrapped function or method.
        schema: OpenAI tool schema generated from the function.
        source: Node representing this tool in the execution graph.
        callback_manager: Manager for handling function execution callbacks.
    """

    def __init__(
        self,
        instance: Any,
        func: Callable[..., Any],
        callback_manager: BaseCallBackManager = BaseCallBackManager(),
    ) -> None:
        """Initialize the function wrapper.

        Args:
            instance: The class instance if this wraps a method, None for
                standalone functions.
            func: The function or method to wrap.
            callback_manager: Manager for handling callbacks.
        """
        self.instance = instance
        self.func = func
        self.schema = get_openai_tool_schema(func)
        self.source: Node = Node(name=self.name, type=NodeType.TOOL)
        self.callback_manager = callback_manager

    @staticmethod
    def wrap(
        func: Callable[..., Any],
        instance: Optional[Any] = None,
        handlers: List[BaseCallBackHandler] = [],
    ) -> Union["SyncFunction", "AsyncFunction"]:
        """Wrap a function or method as either a SyncFunction or AsyncFunction.

        Args:
            func: The function to wrap.
            instance: The class instance if wrapping a method.
            handlers: List of callback handlers.

        Returns:
            Either SyncFunction or AsyncFunction based on the wrapped function
            type.
        """
        if isinstance(func, staticmethod):
            instance = None

        if asyncio.iscoroutinefunction(func) or asyncio.iscoroutinefunction(
            inspect.unwrap(func)
        ):
            return AsyncFunction(
                instance, func, AsyncCallBackManager(handlers=handlers)
            )

        return SyncFunction(
            instance, func, BaseCallBackManager(handlers=handlers)
        )

    @property
    def name(self) -> str:
        """Get the function name from its schema.

        Returns:
            The name of the function as defined in the OpenAI tool schema.
        """
        return cast(str, self.schema["function"]["name"])

    @property
    def description(self) -> str:
        """Get the function description from its schema.

        Returns:
            The description of the function as defined in the OpenAI tool
            schema.
        """
        return cast(str, self.schema["function"]["description"])

    @property
    def parameters(self) -> Dict[str, Any]:
        """Get the function parameters from its schema.

        Returns:
            Dictionary of parameter definitions from the OpenAI tool schema.
        """
        return self.schema["function"]["parameters"]["properties"]  # type: ignore[no-any-return]

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Result[Any, Exception]:
        """Execute the wrapped function.

        Args:
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            Result containing either the return value or an exception.
        """
        ...

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Result[Any, Exception]:
        """Execute the function with callback handling.

        Args:
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            Result containing either the successful return value or an
            exception.
        """
        ...

    @abstractmethod
    def async_run(self, *args: Any, **kwargs: Any) -> Result[Any, Exception]:
        """Execute the function asynchronously with callback handling.

        Args:
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            Result containing either the successful return value or an
            exception.
        """
        ...

    def add_handler(
        self, handler: BaseCallBackHandler, recursive: bool = False
    ) -> None:
        """Add a callback handler to the function's callback manager.

        Args:
            handler: The callback handler to add.
            recursive: Whether to add the handler recursively.
        """
        self.callback_manager.add(handler)


class SyncFunction(BaseFunction):
    """Wrapper for synchronous functions that can be used as tools.

    Implements synchronous execution with callback handling and result
    wrapping.
    """

    def __call__(self, *args: Any, **kwargs: Any) -> Result[Any, Exception]:
        """Execute the wrapped function synchronously.

        Args:
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            Result containing either the successful return value or an
            exception.
        """
        try:
            if self.instance is not None:
                args = (self.instance,) + args
            resp = self.func(*args, **kwargs)
            if isinstance(resp, Result):
                return resp
            return Ok(resp)
        except Exception as e:
            return Err(e, str(e))

    def run(self, *args: Any, **kwargs: Any) -> Result[Any, Exception]:
        """Execute the synchronous function with callback handling.

        Triggers TOOL_START callback before execution and either TOOL_ERROR or
        TOOL_END after.

        Args:
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            Result containing either the successful return value or an
            exception.
        """
        self.callback_manager.call(
            CallBackEvent.TOOL_START, self.source, *args, **kwargs
        )
        result = self(*args, **kwargs)
        if result.is_err:
            self.callback_manager.call(
                CallBackEvent.TOOL_ERROR, self.source, result
            )
        else:
            self.callback_manager.call(
                CallBackEvent.TOOL_END, self.source, result
            )
        return result

    def async_run(self, *args: Any, **kwargs: Any) -> Result[Any, Exception]:
        """Not implemented for synchronous functions.

        Raises:
            NotImplementedError: Always raises this error as sync functions
                cannot be run async.
        """
        raise NotImplementedError("This function is not async")


class AsyncFunction(BaseFunction):
    """Wrapper for asynchronous functions that can be used as tools.

    Implements asynchronous execution with callback handling and result
    wrapping.
    """

    async def __call__(  # type: ignore[override]
        self, *args: Any, **kwargs: Any
    ) -> Result[Any, Exception]:
        """Execute the wrapped function asynchronously.

        Args:
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            Result containing either the successful return value or an
            exception.
        """
        try:
            if self.instance is not None:
                args = (self.instance,) + args
            resp = await self.func(*args, **kwargs)
            if isinstance(resp, Result):
                return resp
            return Ok(resp)
        except Exception as e:
            return Err(e, str(e))

    async def async_run(  # type: ignore[override]
        self, *args: Any, **kwargs: Any
    ) -> Result[Any, Exception]:
        """Execute the asynchronous function with callback handling.

        Triggers TOOL_START callback before execution and either TOOL_ERROR or
        TOOL_END after.

        Args:
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            Result containing either the return value or an exception.
        """
        await CALL_ASYNC_CALLBACK(
            CallBackEvent.TOOL_START, self.source, *args, **kwargs
        )

        result = await self(*args, **kwargs)
        if result.is_err:
            await CALL_ASYNC_CALLBACK(
                CallBackEvent.TOOL_ERROR, self.source, result
            )
        else:
            await CALL_ASYNC_CALLBACK(
                CallBackEvent.TOOL_END, self.source, result
            )
        return result

    def run(self, *args: Any, **kwargs: Any) -> Result[Any, Exception]:
        """Not implemented for asynchronous functions.

        Raises:
            NotImplementedError: Always raises this error as async functions
                cannot be run sync.
        """
        raise NotImplementedError("This function is not sync")


class BaseToolkit(ABC):
    """Abstract base class for creating toolkits that expose multiple functions
    as tools.

    Automatically collects and manages functions marked as tools within the
    class.

    Properties:
        sync_tools: List of synchronous tool functions.
        async_tools: List of asynchronous tool functions.
    """

    def __init__(self) -> None:
        self._exposed_functions = []

        for v in self.__class__.__dict__.values():
            if isinstance(v, BaseFunction):
                if isinstance(v.func, staticmethod):
                    self._exposed_functions.append(v)
                    continue

                v = deepcopy(v)
                if getattr(v, "_flag", False):
                    v.instance = self
                setattr(self, v.name, v)
                self._exposed_functions.append(v)

    @property
    def sync_tools(self) -> List[BaseFunction]:
        """Get all synchronous tools in the toolkit.

        Returns:
            List of all synchronous function tools.
        """
        return [
            f for f in self._exposed_functions if isinstance(f, SyncFunction)
        ]

    @property
    def async_tools(self) -> List[BaseFunction]:
        """Get all asynchronous tools in the toolkit.

        Returns:
            List of all asynchronous function tools.
        """
        return [
            f for f in self._exposed_functions if isinstance(f, AsyncFunction)
        ]
