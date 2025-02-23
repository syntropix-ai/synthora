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
#

from typing import Tuple

import pytest

from synthora.workflows import BaseTask, task
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

    def test_basetask(self):
        def test_func(name: str) -> str:
            return name

        test_task = BaseTask(test_func)
        assert test_task.run("test") == "test"

        test_task_with_name = BaseTask(test_func, name="test_task")
        assert test_task_with_name.name == "test_task"

        test_task_with_immutable = BaseTask(test_func, immutable=True)
        assert test_task_with_immutable.immutable

    async def test_asynctask(self):
        async def test_func(name: str) -> str:
            return name

        def sync_func(name: str) -> str:
            return name

        sync_task = BaseTask(sync_func)
        with pytest.raises(NotImplementedError):
            await sync_task.async_run("test")

        test_task = AsyncTask(test_func)
        assert await test_task.run("test") == "test"
        assert await test_task.async_run("test") == "test"

        test_task_with_name = AsyncTask(test_func, name="test_task")
        assert test_task_with_name.name == "test_task"

        test_task_with_immutable = AsyncTask(test_func, immutable=True)
        assert test_task_with_immutable.immutable

    def test_task_signature(self):
        def test_task(name: str, age: int) -> Tuple[str, int]:
            return name, age

        assert BaseTask(test_task).signature("name", 20).run() == ("name", 20)
        assert BaseTask(test_task).signature(age=20, name="name").run() == (
            "name",
            20,
        )
        assert BaseTask(test_task).signature("name", 20, immutable=True).run(
            "name", 30
        ) == ("name", 20)

        assert BaseTask(test_task).s("name", 20).run() == ("name", 20)
        assert BaseTask(test_task).s(age=20, name="name").run() == ("name", 20)
        assert BaseTask(test_task).si("name", 20).run("name", 30) == (
            "name",
            20,
        )

    def test_task_result(self):
        def test_task(name: str) -> str:
            return name

        test_task = BaseTask(test_task)
        assert test_task.run("name") == "name"
        assert test_task.result() == "name"

    def test_reset(self):
        @task
        def test_task(name: str) -> str:
            return name

        assert test_task.run("name") == "name"
        test_task.reset(clear_arguments=True)
        assert test_task.result() is None
        assert test_task.run("name") == "name"

        test_task.s("name")
        test_task.reset()
        assert test_task.run() == "name"

    def test_task_re_signature(self):
        def test_task(name: str, age: int) -> Tuple[str, int]:
            return name, age

        task = BaseTask(test_task)
        assert task.s("name", 20).run() == ("name", 20)
        assert task.s("name", 30).run() == ("name", 30)
