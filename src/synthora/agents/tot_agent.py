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

from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple, Type, Union, cast

from pydantic import BaseModel, Field

from synthora.agents import BaseAgent
from synthora.callbacks.base_handler import (
    AsyncCallBackHandler,
    BaseCallBackHandler,
)
from synthora.configs.agent_config import AgentConfig
from synthora.configs.model_config import ModelConfig
from synthora.memories.base import BaseMemory
from synthora.memories.full_context_memory import FullContextMemory
from synthora.messages import assistant, system, user
from synthora.messages.base import BaseMessage
from synthora.models import create_model_from_config
from synthora.models.base import BaseModelBackend
from synthora.prompts.base import BasePrompt
from synthora.toolkits.base import BaseFunction
from synthora.types.enums import AgentType, MessageRole, NodeType, Ok, Result
from synthora.types.node import Node
from synthora.utils.macros import (
    FORMAT_PROMPT,
    GET_FINAL_MESSAGE,
    STR_TO_USERMESSAGE,
    UPDATE_SYSTEM,
)
from synthora.workflows.base_task import BaseTask
from synthora.workflows.scheduler.base import BaseScheduler
from synthora.workflows.scheduler.thread_pool import ThreadPoolScheduler


class EvalFormat(BaseModel):
    score: float = Field(
        ...,
        description="The score of the evaluation. Should be between 0 and 1.",
    )
    reason: str = Field(
        ..., description="The brief reason for the evaluation."
    )
    finished: bool = Field(
        ...,
        description="Should be True if the agent can't get the result or should give up, or the agent has finished the task.",
    )


PROPOSE_PROMPT = """
You are an expert problem-solving agent capable of solving problems step by step using the **Think-Observe-Test (TOT)** methodology. Your task is to solve the problem incrementally, executing only **one step at a time** and responding with only one action per step. Each step consists of the following:

1. **Think**: Identify the next logical step in solving the problem.
2. **Observe or Output**:
   - If a tool needs to be called, **Observe** by executing the action and provide the result.
   - If no tool is required, **Output** the result of the current step directly.
3. **Iterate**: Update the problem (if needed) based on the result and prepare for the next step.

---

### Key Rules:
- Each interaction performs only **one step** at a time.
- Respond with **only the result or observation** for the current step.
- Do not attempt to solve the entire problem in one response.
- Stop once the problem is fully resolved.

"""

VALUE_PROMPT = """
You are an evaluation model designed to objectively assess the quality of step-by-step responses provided based on the user's input and the history of the conversation. Your task is to analyze the user's question, compare it with the corresponding response in the history, and provide a score from 0 to 1. The score should reflect how well the response addresses the current step of the user's question in terms of **relevance, completeness for that step**, and clarity.

### Scoring Guidelines:
- **0.0-0.2**: The response is irrelevant to the step, unclear, or introduces significant errors in reasoning.
- **0.3-0.5**: The response partially addresses the current step but lacks clarity or skips minor details necessary for this step.
- **0.6-0.8**: The response is mostly relevant and complete for the current step, with minor issues in clarity or execution.
- **0.9-1.0**: The response fully addresses the current step, is relevant, complete, and clearly advances the problem-solving process.

### Evaluation Adjustments for Step-by-Step Responses:
1. Each response should be evaluated **only for the current step**, not for the overall problem.
2. Do not penalize responses for not solving the full problem; instead, focus on how well they progress the solution at this step.
3. Take into account the logical flow of the step and whether it aligns with the user's input and previous steps in the history.

"""


class ToTAgent(BaseAgent):
    @staticmethod
    def default(  # type: ignore[override]
        propose_prompt: str = PROPOSE_PROMPT,
        value_prompt: str = VALUE_PROMPT,
        finish_threshold: float = 0.9,
        giveup_threshold: float = 0.2,
        search_method: str = "dfs",
        name: str = "TOT",
        model_type: str = "gpt-4o",
        tools: Optional[List[Union["BaseAgent", BaseFunction]]] = None,
        handlers: Optional[
            List[Union[BaseCallBackHandler, AsyncCallBackHandler]]
        ] = None,
    ) -> "ToTAgent":
        r"""Create a default ToT agent with the specified prompt and tools.

        Args:
            propose_prompt:
                The initial prompt for the agent
            value_prompt:
                The initial prompt for the agent
            name:
                The name of the agent. Defaults to "React".
            model_type:
                The model type to use. Defaults to "gpt-4o".
            tools:
                List of available tools. Defaults to [].
            handlers:
                List of callback handlers. Defaults to [].

        Returns:
            The created ToT agent.
        """
        tools = tools or []
        handlers = handlers or []
        config = AgentConfig(
            name=name,
            type=AgentType.TOT,
            model=[
                ModelConfig(model_type=model_type, name=model_type),
                ModelConfig(model_type=model_type, name=model_type),
            ],
            prompt={
                "propose": BasePrompt(propose_prompt),
                "value": BasePrompt(value_prompt),
            },
            tools=tools,
        )
        node = Node(name=name, type=NodeType.AGENT)
        model = create_model_from_config(config.model, node)
        if not isinstance(model, list):
            model = [model, model]
        agent = ToTAgent(
            config,
            Node(name=name, type=NodeType.AGENT),
            model,
            config.prompt,  # type: ignore[arg-type]
            config.tools,  # type: ignore[arg-type]
            finish_threshold=finish_threshold,
            giveup_threshold=giveup_threshold,
            search_method=search_method,
        )
        if handlers:
            for handler in handlers:
                agent.add_handler(handler)
        return agent

    def __init__(
        self,
        config: AgentConfig,
        source: Node,
        model: List[BaseModelBackend],
        prompt: Dict[str, BasePrompt],
        tools: Optional[List[Union["BaseAgent", BaseFunction]]] = None,
        level_size: int = 3,
        max_turns: int = 5,
        finish_threshold: float = 0.9,
        giveup_threshold: float = 0.2,
        search_method: str = "dfs",
    ) -> None:
        tools = tools or []
        super().__init__(config, source, model, prompt, tools)
        if len(self.model) != 2:  # type: ignore[arg-type]
            raise ValueError(
                "ToTAgent agent requires two models, first for proposing and"
                " second for value."
            )
        if not isinstance(prompt, dict):
            raise ValueError(
                "ToTAgent agent requires a dictionary of prompts."
            )

        self.propose_model = model[0]
        self.value_model = model[1]

        self.value_model.config["response_format"] = EvalFormat
        if "stream" in self.value_model.config:
            del self.value_model.config["stream"]

        self.propose_model.config["tools"] = [tool.schema for tool in tools]

        self.propose_prompt = prompt.get("propose", PROPOSE_PROMPT)
        self.value_prompt = prompt.get("value", VALUE_PROMPT)

        self.level_size = level_size
        self.max_turns = max_turns
        self.finish_threshold = finish_threshold
        self.giveup_threshold = giveup_threshold

        self.states: List[List[BaseMemory]] = []
        self.scores: List[List[float]] = []
        self.visited: List[List[bool]] = []
        self.search_method = search_method
        self.history = FullContextMemory()
        self.cursor = 0

    def step(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Any
    ) -> Result[List[BaseMessage], Exception]:
        UPDATE_SYSTEM(prompt=FORMAT_PROMPT(prompt=self.propose_prompt))
        message = cast(BaseMessage, STR_TO_USERMESSAGE())
        if message.content:
            self.history.append(message)

        scheduler = ThreadPoolScheduler()
        tasks: List[Union[BaseTask, BaseScheduler]] = [
            BaseTask(deepcopy(self.propose_model).run).si(
                self.history, *args, **kwargs
            )
            for _ in range(self.level_size)
        ]
        scheduler.add_task_group(tasks)
        resps = [GET_FINAL_MESSAGE(x) for x in scheduler.run()]

        return Ok(resps)

    def _get_eval_workflow(
        self,
        scheduler: Type[BaseScheduler],
        user_message: Union[BaseMessage, str],
    ) -> BaseScheduler:
        tasks: List[Union[BaseTask, BaseScheduler]] = []
        for state in self.states[self.cursor][-self.level_size :]:
            query_str = (
                user_message.content
                if isinstance(user_message, BaseMessage)
                else user_message
            )
            tasks.append(
                BaseTask(self.value_model.run).si(
                    FullContextMemory(
                        [
                            system(self.value_prompt),
                            *state,
                            user(f"The query is: {query_str}"),
                        ]
                    )
                )
            )
        workflow = scheduler()
        workflow.add_task_group(tasks)
        return workflow

    def run(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Any
    ) -> Result[Any, Exception]:
        """Execute the complete ReAct agent reasoning and action loop.

        Processes the input message and continues executing steps until either:
        - A final answer is reached
        - The 'finish' tool is called
        - An error occurs

        Args:
            message (Union[str, BaseMessage]): Input message to process
            *args (Any): Additional positional arguments
            **kwargs (Dict[str, Any]): Additional keyword arguments

        Returns:
            Result[Any, Exception]: A Result containing either:
                - The final response string
                - An Exception if the execution failed
        """
        message = cast(BaseMessage, STR_TO_USERMESSAGE())
        self.on_start(message)
        for _turn in range(self.max_turns):
            if len(self.states) <= self.cursor:
                self.states.append([])
                self.scores.append([])
                self.visited.append([])
            response = self.step(message, *args, **kwargs)
            message = ""
            if response.is_err:
                self.on_error(response)
                return response

            datas = response.unwrap()

            for data in datas:
                self.states[self.cursor].append(self.history + [data])
                self.visited[self.cursor].append(False)
                if not data.tool_calls:
                    continue
                for tool_call in data.tool_calls:
                    func = tool_call.function
                    try:
                        tool = self.get_tool(func.name)
                        resp = self.call_tool(func.name, func.arguments)
                        resp_value = resp.unwrap()
                    except Exception as e:
                        resp_value = f"Error: {str(e)}"
                        self.on_error(resp)

                    self.states[self.cursor][-1].append(
                        BaseMessage.create_message(
                            id=tool_call.id,
                            role=MessageRole.TOOL_RESPONSE,
                            content=resp_value,
                            source=tool.source,
                        )
                    )
            workflow = self._get_eval_workflow(ThreadPoolScheduler, message)
            resps = [GET_FINAL_MESSAGE(x) for x in workflow.run()]
            for idx, resp in enumerate(resps):
                try:
                    self.scores[self.cursor].append(resp.parsed.score)  # type: ignore
                    if (
                        self.scores[self.cursor][-1] >= self.finish_threshold
                        and resp.parsed.finished  # type: ignore
                    ):
                        result = self.states[self.cursor][
                            len(resps) - self.level_size + idx
                        ][-1]
                        if result.role == MessageRole.ASSISTANT:
                            result = result.content
                            self.on_end(result)
                            return Ok(result)
                except Exception:
                    self.scores[-1].append(0.0)
            self._set_next_state()
        self.on_end(
            assistant("The agent has reached the maximum number of turns.")
        )
        return Ok("The agent has reached the maximum number of turns.")

    def _set_next_state(self) -> None:
        if self.search_method == "dfs":
            while self.cursor >= 0:
                for idx, state in enumerate(self.states[self.cursor]):
                    if (
                        not self.visited[self.cursor][idx]
                        and self.scores[self.cursor][idx]
                        >= self.giveup_threshold
                    ):
                        self.visited[self.cursor][idx] = True
                        self.history = state
                        self.cursor += 1
                        return
                self.cursor -= 1
            raise Exception("No valid state found.")
        elif self.search_method == "bfs":
            if not (queue := getattr(self, "_queue", None)):
                self._queue: List[Tuple[List[BaseMemory], int]] = []
                queue = self._queue
            for idx, state in enumerate(self.states[self.cursor]):
                if (
                    not self.visited[self.cursor][idx]
                    and self.scores[self.cursor][idx] >= self.giveup_threshold
                ):
                    self.visited[self.cursor][idx] = True
                    queue.append((state, self.cursor))
            if queue:
                self.history, self.cursor = queue.pop(0)
                self.cursor += 1
                return
            raise Exception("No valid state found.")

    async def async_step(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Any
    ) -> Result[Any, Exception]:
        """Execute a single step of the ReAct agent asynchronously.

        Note: This is a placeholder for future async implementation.

        Args:
            message (Union[str, BaseMessage]): Input message to process
            *args (Any): Additional positional arguments
            **kwargs (Dict[str, Any]): Additional keyword arguments

        Returns:
            Result[Any, Exception]: A Result containing either:
                - The step execution result
                - An Exception if the step failed
        """
        raise NotImplementedError(
            "Async step execution is not yet implemented."
        )

    async def async_run(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Any
    ) -> Result[Any, Exception]:
        raise NotImplementedError(
            "Async run execution is not yet implemented."
        )
