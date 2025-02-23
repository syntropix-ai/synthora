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


from synthora.workflows import (
    AsyncTask,
    BaseScheduler,
    BaseTask,
    ProcessPoolScheduler,
    ThreadPoolScheduler,
)


def add(a: int, b: int) -> int:
    print(f"Adding {a} and {b}")
    return a + b


def add_one(a: int) -> int:
    return a + 1


class TestSchedulers:
    def test_linear_workflow(self):
        flow = BaseTask(add).si(1, 2) >> BaseTask(add).s(3)
        assert flow.run() == 6

        flow = (
            ThreadPoolScheduler()
            >> BaseTask(add).si(1, 2)
            >> BaseTask(add).s(3)
        )
        assert flow.run() == 6

        flow = (
            ProcessPoolScheduler()
            >> BaseTask(add).si(1, 2)
            >> BaseTask(add).s(3)
        )

        assert flow.run() == 6

    def test_parallel_workflow(self):
        flow = (
            BaseTask(add).si(1, 2) | BaseTask(add).si(3, 4)
        ).set_flat_result(True) >> BaseTask(add)
        assert flow.run() == 10

        flow = (
            ThreadPoolScheduler()
            | BaseTask(add).si(1, 2)
            | BaseTask(add).si(3, 4)
        ).set_flat_result(True) >> BaseTask(add)
        assert flow.run() == 10

        flow = (
            ProcessPoolScheduler()
            | BaseTask(add).si(1, 2)
            | BaseTask(add).si(3, 4)
        ).set_flat_result(True) >> BaseTask(add)
        assert flow.run() == 10

    def test_nested_workflow(self):
        flow1 = (
            BaseScheduler() | BaseTask(add).si(1, 1) | BaseTask(add).si(1, 2)
        )
        flow1.set_flat_result(True)

        flow2 = BaseTask(add).s(1) >> flow1 >> BaseTask(add) | BaseTask(
            add
        ).si(1, 2)

        assert isinstance(flow2, BaseScheduler)
        assert flow2.run(1) == [5, 3]

        flow2 = ThreadPoolScheduler() >> BaseTask(add).s(
            1
        ) >> flow1 >> BaseTask(add) | BaseTask(add).si(1, 2)
        assert isinstance(flow2, ThreadPoolScheduler)
        assert flow2.run(1) == [5, 3]

        flow2 = ProcessPoolScheduler() >> BaseTask(add).s(
            1
        ) >> flow1 >> BaseTask(add) | BaseTask(add).si(1, 2)
        assert isinstance(flow2, ProcessPoolScheduler)
        assert flow2.run(1) == [5, 3]

    def test_workflow_signature(self):
        flow = BaseTask(add) >> BaseTask(add).s(3)
        assert flow.s(1, 2).run() == 6
        assert flow.reset().s(5, 6).run() == 14

        flow = BaseTask(add) >> BaseTask(add).s(3)
        assert flow.signature(1, 2).run() == 6
        assert flow.reset().signature(5, 6).run() == 14

    def test_workflow_immutable(self):
        flow = (BaseTask(add).si(1, 2) >> BaseTask(add).s(3)).set_immutable(
            True
        )
        assert flow.immutable
        assert flow.run(5, 6) == 6

        flow = BaseTask(add) >> BaseTask(add).s(3)
        assert flow.si(1, 2).run(5, 6) == 6

        flow = BaseTask(add) >> BaseTask(add).s(3)
        assert flow.signature(1, 2, immutable=True).run(5, 6) == 6

    def test_workflow_flat_result(self):
        flow = (
            BaseScheduler() | BaseTask(add).si(1, 2) | BaseTask(add).si(1, 2)
        )
        flow.set_flat_result(True)
        assert flow.flat_result

        flow2 = flow >> BaseTask(add)
        assert flow2.run() == 6

        flow = BaseTask(add).si(1, 2) | BaseTask(add).si(1, 2)
        assert not flow.flat_result

        flow2 = flow >> BaseTask(add)
        assert flow2.run() is None

    def test_workflow_chain(self):
        test_task1 = BaseTask(add).si(1, 2)
        test_task2 = BaseTask(add).s(3)
        test_task3 = BaseTask(add).s(5)

        flow = BaseScheduler.chain(test_task1, test_task2, test_task3)
        assert flow.run() == 11

        flow = ThreadPoolScheduler.chain(test_task1, test_task2, test_task3)
        assert flow.run() == 11

        flow = ProcessPoolScheduler.chain(test_task1, test_task2, test_task3)
        assert flow.run() == 11

    def test_workflow_group(self):
        test_task1 = BaseTask(add).s(1)
        test_task2 = BaseTask(add).s(3)
        test_task3 = BaseTask(add).s(5)

        flow = BaseScheduler.group(test_task1, test_task2, test_task3)
        assert flow.run(2) == [3, 5, 7]

        flow = ThreadPoolScheduler.group(test_task1, test_task2, test_task3)
        assert flow.run(2) == [3, 5, 7]

        flow = ProcessPoolScheduler.group(test_task1, test_task2, test_task3)
        assert flow.run(2) == [3, 5, 7]

    def test_workflow_starmap(self):
        test_task = BaseTask(add)
        flow = BaseScheduler.starmap(test_task, [(1, 2), (3, 4), (5, 6)])
        assert flow.run() == [3, 7, 11]

        flow = ThreadPoolScheduler.starmap(test_task, [(1, 2), (3, 4), (5, 6)])
        assert flow.run() == [3, 7, 11]

        flow = ProcessPoolScheduler.starmap(
            test_task, [(1, 2), (3, 4), (5, 6)]
        )
        assert flow.run() == [3, 7, 11]

    def test_workflow_map(self):
        test_task = BaseTask(add_one)
        flow = BaseScheduler.map(test_task, [1, 2, 3])
        assert flow.run() == [2, 3, 4]

        flow = ThreadPoolScheduler.map(test_task, [1, 2, 3])
        assert flow.run() == [2, 3, 4]

        flow = ProcessPoolScheduler.map(test_task, [1, 2, 3])
        assert flow.run() == [2, 3, 4]

    async def test_async_workflow(self):
        async def add_async(a: int, b: int) -> int:
            return a + b

        test_task1 = AsyncTask(add_async).si(1, 2)
        test_task2 = AsyncTask(add_async).s(3)

        flow = test_task1 >> test_task2
        assert await flow.async_run() == 6
