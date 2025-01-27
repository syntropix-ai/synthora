from abc import ABC, abstractmethod
import datetime
from enum import Enum
import threading
import time
from typing import Any, Dict, Literal, Optional, Self, Union

from synthora.agents.base import BaseAgent
from synthora.toolkits.base import BaseFunction
from synthora.triggers.base import BaseTrigger
from synthora.types.enums import Ok, Result, TriggerRuntime
from synthora.utils.pydantic_model import get_pydantic_model
from pydantic import BaseModel, Field
import asyncio
import apscheduler
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from pydantic import BaseModel, Field
from datetime import datetime


class APSchedulerTriggerArgs(BaseModel):
    """
    Model for the 'cron' trigger.
    """

    trigger: str = Field(..., description="Trigger type: cron. Should be 'cron'")
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
    end_date: Optional[datetime] = Field(None, description="End date/time for the job.")


class APSchedulerTrigger(BaseTrigger):

    def __init__(
        self, args_name: str = "__time", scheduler: Optional[BaseScheduler] = None
    ):
        super().__init__(args_name)
        self.scheduler = scheduler or BackgroundScheduler()
        self.jobs = []

    def add(self, obj: Union[BaseFunction, BaseAgent]) -> Self:
        if self.args_name in obj.schema["function"]["parameters"]["properties"]:
            raise ValueError(f"Parameter {self.args_name} already exists in {obj.name}")
        obj.schema["function"]["parameters"]["properties"][
            self.args_name
        ] = APSchedulerTriggerArgs.model_json_schema()
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

        obj.run = run
        _async_run = obj.async_run

        async def async_run(*args: Any, **kwargs: Any) -> Result[str, Exception]:
            trigger_args = kwargs.get(self.args_name, None)
            if self.args_name in kwargs:
                del kwargs[self.args_name]
            if not trigger_args:
                return await _async_run(*args, **kwargs)
           
            job = self.scheduler.add_job(
                obj.async_run, **trigger_args, args=args, kwargs=kwargs
            )
            self.jobs.append(job)
            return Ok(f"Task {obj.name} added successfully!")

        obj.async_run = async_run

        return self

    def start(self):
        self.scheduler.start()

    def stop(self, wait: bool = True):
        self.scheduler.shutdown(wait=wait)
