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

import random
from typing import Any, Callable, Optional

from synthora.workflows import task
from synthora.workflows.base_task import BaseTask
from synthora.workflows.context.base import BaseContext


def for_loop(
    task_name_or_offset: str, num: int, counter_name: Optional[str] = None
) -> BaseTask:
    counter_name = (
        counter_name
        or f"{task_name_or_offset}_counter_{num}"
        + "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=5))
    )
    num = int(num)
    if num <= 0:
        raise ValueError("Number of iterations must be greater than 0.")

    @task
    def _loop(context: BaseContext, *args: Any, **kwargs: Any) -> Any:
        if counter_name not in context:
            context[counter_name] = num - 1
        if context[counter_name] <= 0:
            if kwargs:
                return *args, kwargs
            return args
        context[counter_name] = context[counter_name] - 1
        if isinstance(task_name_or_offset, int):
            if task_name_or_offset >= 0:
                raise ValueError("Offset must be negative.")
            cursor = context.get_cursor() + task_name_or_offset - 1
            context.set_cursor(cursor)
        else:
            workflow = context.workflow.get_workflow_by_task(
                task_name_or_offset
            )
            if not workflow:
                raise ValueError(f"Task {task_name_or_offset} not found.")
            for idx, task_grop in enumerate(workflow.tasks):
                if len(task_grop) != 1:
                    continue
                if task_grop[0].name == task_name_or_offset:
                    cursor = idx - 1
                    context.set_cursor(cursor)
                    break
            else:
                raise ValueError(f"Task {task_name_or_offset} not found.")

    return _loop


def while_loop(
    task_name_or_offset: str, condition_func: Callable[..., bool]
) -> BaseTask:
    @task
    def _loop(context: BaseContext, *args: Any, **kwargs: Any) -> Any:
        condition = condition_func(context, *args, **kwargs)
        if not condition:
            if kwargs:
                return *args, kwargs
            return args
        if isinstance(task_name_or_offset, int):
            cursor = context.get_cursor() + task_name_or_offset
            context.set_cursor(cursor)
        else:
            workflow = context.workflow.get_workflow_by_task(
                task_name_or_offset
            )
            if not workflow:
                raise ValueError(f"Task {task_name_or_offset} not found.")
            for idx, task_grop in enumerate(workflow.tasks):
                if len(task_grop) != 1:
                    continue
                if task_grop[0].name == task_name_or_offset:
                    cursor = idx - 1
                    context.set_cursor(cursor)
                    break
            else:
                raise ValueError(f"Task {task_name_or_offset} not found.")

    return _loop
