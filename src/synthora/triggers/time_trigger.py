# LICENSE HEADER MANAGED BY add-license-header
#
# Copyright 2024-2025 Syntropix-AI.org
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

import asyncio
import time
from datetime import datetime
from threading import Thread
from typing import Any, Dict, List, Optional, Self, Tuple, Union

from pydantic import BaseModel, Field

from synthora.agents.base import BaseAgent
from synthora.toolkits.base import BaseFunction
from synthora.triggers.base import BaseTrigger
from synthora.types.enums import Ok, Result, TriggerRuntime


class TimeTriggerArgs(BaseModel):
    trigger_time: Optional[str] = Field(
        ...,
        description="""The time to trigger the function,
        in the format of 'YYYY-MM-DD HH:MM:SS' if the function is
        triggered at a specific time. else, leave it empty.""",
    )


class TimeTrigger(BaseTrigger):
    def __init__(self, args_name: str = "__time", beat: float = 5.0):
        super().__init__(args_name)
        self.beat = beat
        self.thread: Optional[Thread] = None
        self.tasks: List[
            Tuple[
                datetime,
                Union[BaseFunction, BaseAgent],
                TriggerRuntime,
                Tuple[Any],
                Dict[str, Any],
            ]
        ] = []
        self.flag = False
        self.wait = True

    def add(self, obj: Union[BaseFunction, BaseAgent]) -> Self:
        if (
            self.args_name
            in obj.schema["function"]["parameters"]["properties"]  # type: ignore[index]
        ):
            raise ValueError(
                f"Parameter {self.args_name} already exists in {obj.name}"
            )
        obj.schema["function"]["parameters"]["properties"][self.args_name] = (  # type: ignore[index]
            TimeTriggerArgs.model_json_schema()
        )
        _run = obj.run

        def run(*args: Any, **kwargs: Any) -> Result[str, Exception]:
            trigger_time = kwargs.get(self.args_name, {}).get(
                "trigger_time", None
            )

            if self.args_name in kwargs:
                del kwargs[self.args_name]
            if not trigger_time:
                return _run(*args, **kwargs)

            self.tasks.append(
                (
                    datetime.strptime(trigger_time, "%Y-%m-%d %H:%M:%S"),
                    obj,
                    TriggerRuntime.SYNC,
                    args,
                    kwargs,
                )
            )
            return Ok(f"Task {obj.name} added successfully!")

        obj.run = run  # type: ignore[method-assign]
        _async_run = obj.async_run

        async def async_run(
            *args: Any, **kwargs: Any
        ) -> Result[str, Exception]:
            trigger_time = kwargs.get(self.args_name, None)
            if self.args_name in kwargs:
                del kwargs[self.args_name]
            if not trigger_time:
                return await _async_run(*args, **kwargs)  # type: ignore[no-any-return]

            self.tasks.append(
                (
                    datetime.strptime(trigger_time, "%Y-%m-%d %H:%M:%S"),
                    obj,
                    TriggerRuntime.ASYNC,
                    args,
                    kwargs,
                )
            )
            return Ok(f"Task {obj.name} added successfully!")

        obj.async_run = async_run  # type: ignore[method-assign]

        return self

    def _run(self) -> None:
        loop = None
        while True:
            if self.flag and len(self.tasks) == 0:
                break
            if not self.wait:
                break
            self.tasks.sort(key=lambda x: x[0])
            while len(self.tasks) > 0 and datetime.now() >= self.tasks[0][0]:
                task = self.tasks.pop(0)
                _, obj, runtime, args, kwargs = task
                if runtime == TriggerRuntime.SYNC:
                    obj.run(*args, **kwargs)
                else:
                    if not loop:
                        try:
                            loop = asyncio.get_event_loop()
                        except RuntimeError:
                            loop = asyncio.new_event_loop()
                        except Exception as e:
                            raise e
                    loop.run_until_complete(obj.async_run(*args, **kwargs))  # type: ignore
                continue
            else:
                time.sleep(self.beat)

    def start(self) -> Self:
        thread = Thread(target=self._run, daemon=True)
        thread.start()
        self.thread = thread
        return self

    def stop(self, wait: bool = True) -> Self:
        if not self.thread:
            return self
        self.flag = True
        self.wait = wait
        self.thread.join()
        self.thread = None
        self.flag = False
        self.wait = True
        return self
