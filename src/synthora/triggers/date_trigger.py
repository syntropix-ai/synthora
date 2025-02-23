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


from datetime import datetime
from typing import Any, List, Optional, Union


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import BaseScheduler, Job
from pydantic import BaseModel, Field

from synthora.agents.base import BaseAgent
from synthora.toolkits.base import BaseFunction
from synthora.triggers.base import BaseTrigger
from synthora.types.enums import Ok, Result


class DateTriggerArgs(BaseModel):
    """
    Model for the 'date' trigger.
    """

    trigger: str = Field(
        ..., description="Trigger type: date. Should be 'date'"
    )
    run_date: datetime = Field(..., description="The time to run the function")


class DateTrigger(BaseTrigger):
    r"""A trigger that schedules a function to run at a specific time

    The trigger uses the `APScheduler <https://apscheduler.readthedocs.io/en/stable/>`_
    library to schedule the function to run at a specific time. The trigger
    uses the specified time to schedule the function and runs the function.

    Attributes:
        args_name:
            The name of the argument that will be added to the function
            or agent to specify the time to run the function.
            Defaults to '__time'.
        scheduler:
            The scheduler to use to schedule the function. Defaults to None.
    """

    def __init__(
        self,
        args_name: str = "__time",
        scheduler: Optional[BaseScheduler] = None,
    ):
        super().__init__(args_name)
        self.scheduler = scheduler or BackgroundScheduler()
        self.jobs: List[Job] = []

    def add(self, obj: Union[BaseFunction, BaseAgent]) -> Self:
        r"""Add a function or agent to the trigger

        Args:
            obj:
                The function or agent to be added to the trigger.

        Returns:
            Self: The trigger object with the function or agent added.
        """
        if (
            self.args_name
            in obj.schema["function"]["parameters"]["properties"]  # type: ignore[index]
        ):
            raise ValueError(
                f"Parameter {self.args_name} already exists in {obj.name}"
            )
        obj.schema["function"]["parameters"]["properties"][self.args_name] = (  # type: ignore[index]
            DateTriggerArgs.model_json_schema()
        )
        _run = obj.run

        def run(*args: Any, **kwargs: Any) -> Result[str, Exception]:
            trigger_args = kwargs.get(self.args_name, {})
            if self.args_name in kwargs:
                del kwargs[self.args_name]
            if not trigger_args:
                return _run(*args, **kwargs)
            job = self.scheduler.add_job(
                obj.run, **trigger_args, args=args, kwargs=kwargs
            )
            self.jobs.append(job)
            return Ok(f"Task {obj.name} added successfully!")

        obj.run = run  # type: ignore[method-assign]
        _async_run = obj.async_run

        async def async_run(
            *args: Any, **kwargs: Any
        ) -> Result[str, Exception]:
            trigger_args = kwargs.get(self.args_name, None)
            if self.args_name in kwargs:
                del kwargs[self.args_name]
            if not trigger_args:
                return await _async_run(*args, **kwargs)  # type: ignore

            job = self.scheduler.add_job(
                obj.async_run, **trigger_args, args=args, kwargs=kwargs
            )
            self.jobs.append(job)
            return Ok(f"Task {obj.name} added successfully!")

        obj.async_run = async_run  # type: ignore[method-assign]

        return self

    def start(self) -> Self:
        r"""Start the scheduler

        Returns:
            Self: The trigger object with the scheduler started.
        """
        self.scheduler.start()
        return self

    def stop(self, wait: bool = True) -> Self:
        r"""Stop the scheduler

        Args:
            wait:
                Whether to wait for the scheduler to stop before returning.
                Defaults to True.

        Returns:
            Self: The trigger object with the scheduler stopped.
        """
        self.scheduler.shutdown(wait=wait)
        return self
