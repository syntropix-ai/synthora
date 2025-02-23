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


class CronTriggerArgs(BaseModel):
    """
    Model for the 'cron' trigger.
    """

    trigger: str = Field(
        ..., description="Trigger type: cron. Should be 'cron'"
    )
    year: Optional[Union[str, int]] = Field(
        "*", description="Year, can be a specific year or '*'"
    )
    month: Optional[Union[str, int]] = Field(
        "*", description="Month, can be a specific month or '*'"
    )
    day: Optional[Union[str, int]] = Field(
        "*", description="Day, can be a specific day or '*'"
    )
    week: Optional[Union[str, int]] = Field(
        "*", description="Week, can be a specific week or '*'"
    )
    day_of_week: Optional[Union[str, int]] = Field(
        "*", description="Day of the week, can be a range or '*'"
    )
    hour: Optional[Union[str, int]] = Field(
        "*", description="Hour, can be a specific hour or '*'"
    )
    minute: Optional[Union[str, int]] = Field(
        "*", description="Minute, can be a specific minute or '*'"
    )
    second: Optional[Union[str, int]] = Field(
        "*", description="Second, can be a specific second or '*'"
    )
    start_date: Optional[datetime] = Field(
        None, description="Start date/time for the job"
    )
    end_date: Optional[datetime] = Field(
        None, description="End date/time for the job."
    )


class CronTrigger(BaseTrigger):
    r"""A trigger that schedules a function to run at a specific time

    The trigger uses the `APScheduler <https://apscheduler.readthedocs.io/en/stable/>`_
    library to schedule the function to run at a specific time. The trigger
    uses the cron syntax to specify the time at which the function should be
    run.

    Attributes:
        args_name:
            The name of the argument that will be used to pass the trigger
            arguments to the function. Defaults to '__time'.
        scheduler:
            The scheduler to use for scheduling the function. Defaults to
            a BackgroundScheduler.
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
        r"""Add the trigger to the function or agent

        Args:

            obj:
                The function or agent to which the trigger should be added.

        Returns:
            Self: The trigger object with the trigger added
                to the function or agent.
        """
        if (
            self.args_name
            in obj.schema["function"]["parameters"]["properties"]  # type: ignore[index]
        ):
            raise ValueError(
                f"Parameter {self.args_name} already exists in {obj.name}"
            )
        obj.schema["function"]["parameters"]["properties"][self.args_name] = (  # type: ignore[index]
            CronTriggerArgs.model_json_schema()
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
