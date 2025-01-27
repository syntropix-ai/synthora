from abc import ABC, abstractmethod
import datetime
import threading
import time
from typing import Any, Dict, Optional, Self, Union

from synthora.agents.base import BaseAgent
from synthora.toolkits.base import BaseFunction
from synthora.triggers.base import BaseTrigger
from synthora.types.enums import Ok, Result, TriggerRuntime
from synthora.utils.pydantic_model import get_pydantic_model
from pydantic import BaseModel, Field
import asyncio

class TimeTriggerArgs(BaseModel):
    trigger_time: Optional[str] = Field(..., description="The time to trigger the function, in the format of 'YYYY-MM-DD HH:MM:SS' if the function is triggered at a specific time. else, leave it empty.")

class TimeTrigger(BaseTrigger):
    def __init__(self, args_name: str = "time", beat: float = 5.0):
        super().__init__(args_name)
        self.beat = beat
        self.thread = None
        self.tasks = []
        self.flag = False

    def add(
        self, obj: Union[BaseFunction, BaseAgent]
    ) -> Self:
        if self.args_name in obj.schema["function"]["parameters"]["properties"]:
            raise ValueError(f"Parameter {self.args_name} already exists in {obj.name}")
        obj.schema["function"]["parameters"]["properties"][
            self.args_name
        ] = TimeTriggerArgs.model_json_schema()
        _run = obj.run
        def run(**kwargs: Any) -> Result[str, Exception]:
            trigger_time = kwargs.get(self.args_name, {}).get("trigger_time", None)
            
            if self.args_name in kwargs:
                del kwargs[self.args_name]
            if not trigger_time:
                return _run(**kwargs)

            trigger_time = datetime.datetime.strptime(trigger_time, "%Y-%m-%d %H:%M:%S")
            self.tasks.append((trigger_time, obj, TriggerRuntime.SYNC, kwargs))
            return Ok(f"Task {obj.name} added successfully!")
        obj.run = run
        _async_run = obj.async_run
        async def async_run(**kwargs: Any) -> Result[str, Exception]:
            trigger_time = kwargs.get(self.args_name, None)
            if self.args_name in kwargs:
                del kwargs[self.args_name]
            if not trigger_time:
                return await _async_run(**kwargs)

            trigger_time = datetime.datetime.strptime(trigger_time, "%Y-%m-%d %H:%M:%S")
            self.tasks.append((trigger_time, obj, TriggerRuntime.ASYNC, kwargs))
            return Ok(f"Task {obj.name} added successfully!")
        obj.async_run = async_run

        return self

    def _run(self):
        loop = None
        while True:
            if self.flag and len(self.tasks) == 0:
                break
            self.tasks.sort(key=lambda x: x[0])
            while len(self.tasks) > 0 and datetime.datetime.now() >= self.tasks[0][0]:
                task = self.tasks.pop(0)
                _, obj, runtime, kwargs = task
                if runtime == TriggerRuntime.SYNC:
                    obj.run(**kwargs)
                else:
                    if not loop:
                        try:
                            loop = asyncio.get_event_loop()
                        except RuntimeError:
                            loop = asyncio.new_event_loop()
                        except Exception as e:
                            raise e
                    loop.run_until_complete(obj.async_run(**kwargs))
                continue
            else:
                time.sleep(self.beat)

    def start(self):
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self.flag = True
        self.thread.join()
        self.thread = None
        self.flag = False
