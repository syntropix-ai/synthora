from typing import List, Tuple
import pytest

from synthora.workflows import task, BaseTask
from synthora.workflows.base_task import AsyncTask


class TestTasks:
    def test_decorater(self):

        @task
        def test_task() -> str:
            return "test"
        
        @task
        def test_task_with_args(arg1: str, arg2: int) -> Tuple[str, int]:
            return arg1, arg2
        
        assert isinstance(test_task, BaseTask)
        assert isinstance(test_task_with_args, BaseTask)
    
    def test_decorator_with_name(self):

        @task(name="test_task")
        def test_task() -> str:
            return "test"
        
        assert test_task.name == "test_task"
    
    def test_decorator_with_immutable(self):
        
        @task(immutable=True)
        def test_task(name: str) -> str:
            return name
        

        assert test_task.immutable

        with pytest.raises(TypeError):
            test_task.run()
        
        with pytest.raises(TypeError):
            test_task.run("test")
        
        test_task.s("signature")
        assert test_task.run() == "signature"
        assert test_task.run("test") == "signature"
    
    async def test_decorator_with_async_func(self):

        @task
        async def test_task() -> str:
            return "test"
        
        assert isinstance(test_task, AsyncTask)
        assert await test_task.run() == "test"
        
        
    

    
