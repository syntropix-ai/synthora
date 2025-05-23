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

from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple, Type, Union, cast


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

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
from synthora.messages import system, user
from synthora.messages.base import BaseMessage
from synthora.models import create_model_from_config
from synthora.models.base import BaseModelBackend
from synthora.prompts.base import BasePrompt
from synthora.prompts.buildin import (
    ZeroShotTOTEvalPrompt,
    ZeroShotTOTProposePrompt,
)
from synthora.toolkits.base import BaseFunction
from synthora.types.enums import (
    AgentType,
    Err,
    MessageRole,
    NodeType,
    Ok,
    Result,
)
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
        description="Should be True if the agent can't get the result or"
        + " should give up, or the agent has finished the task.",
    )


class ToTAgent(BaseAgent):
    r"""A ToT (Tree of Thoughts) agent that
    can solve problems incrementally.
    """

    @staticmethod
    def default(  # type: ignore[override]
        propose_prompt: str = ZeroShotTOTProposePrompt,
        value_prompt: str = ZeroShotTOTEvalPrompt,
        level_size: int = 3,
        max_turns: int = 5,
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
            prompt: The initial prompt for the agent
            name: The name of the agent. Defaults to "React".
            model_type: The model type to use. Defaults to "gpt-4o".
            tools: List of available tools. Defaults to [].
            handlers: List of callback handlers. Defaults to [].

        Returns:
            ToTAgent: The created ToT agent
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
            level_size=level_size,
            max_turns=max_turns,
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
        r"""Initialize a ToT agent with the specified configuration.

        Args:
            config: The agent configuration.
            source: The source node of the agent.
            model: The models to use, should be a list of two models,
                first for proposing and second for value.
                When only one model is provided,
                it will be used for both proposing and value.
            prompt: The prompts to use,
                should be a dictionary with keys "propose" and "value".
            tools: The tools to use, should be a list of tools or agents.
            level_size: The size of each level in the search tree.
            max_turns: The maximum number of turns to run the agent.
            finish_threshold: The threshold for finishing the task.
                Should be between 0 and 1.
            giveup_threshold: The threshold for giving up on a task.
                Should be between 0 and 1.
            search_method: The search method to use,
                should be either "dfs" or "bfs".
        """
        tools = tools or []
        super().__init__(config, source, model, prompt, tools)
        if len(self.model) != 2:  # type: ignore[arg-type]
            raise ValueError(
                "ToTAgent agent requires two models,"
                "first for proposing and second for value."
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

        self.propose_prompt = BasePrompt(
            prompt.get("propose", ZeroShotTOTProposePrompt)
        )
        self.value_prompt = BasePrompt(
            prompt.get("value", ZeroShotTOTEvalPrompt)
        )

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
        r"""Execute a single step of the ToT agent reasoning and action loop.

        Args:
            message: The input message to process.
            *args: Additional positional arguments to pass to the model.
            **kwargs: Additional keyword arguments to pass to the model.

        Returns:

            Result: A Result containing either:
                - The final response string
                - An Exception if the execution failed

        """
        UPDATE_SYSTEM(prompt=FORMAT_PROMPT(prompt=self.propose_prompt))
        for _args in self.propose_prompt.args:
            if _args in kwargs:
                del kwargs[_args]
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
        results = scheduler.run()
        if not isinstance(results, list):
            results = [results]
        resps = [GET_FINAL_MESSAGE(x) for x in results]
        return Ok(resps)

    def _get_eval_workflow(
        self,
        scheduler: Type[BaseScheduler],
        user_message: Union[BaseMessage, str],
    ) -> BaseScheduler:
        r"""Get the evaluation workflow for the ToT agent.

        Args:
            scheduler: The scheduler to use for the evaluation.
            user_message: The user message to evaluate.

        Returns:
            BaseScheduler: The evaluation workflow.
        """
        tasks: List[Union[BaseTask, BaseScheduler]] = []
        for state in self.states[self.cursor][-self.level_size :]:
            query = (
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
                            user(f"The query is:{query}"),
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
        _ori_message = deepcopy(message)
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
                self.states[self.cursor].append(
                    FullContextMemory(self.history + [data])
                )
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
                        try:
                            self.on_error(resp)
                        except Exception as _:
                            self.on_error(Err(e, resp_value))

                    self.states[self.cursor][-1].append(
                        BaseMessage.create_message(
                            id=tool_call.id,
                            tool_response=resp_value,
                            role=MessageRole.TOOL_RESPONSE,
                            content=str(resp_value),
                            source=tool.source,
                        )
                    )

            workflow = self._get_eval_workflow(
                ThreadPoolScheduler, _ori_message
            )
            _results = workflow.run()
            if not isinstance(_results, list):
                _results = [_results]
            resps = [GET_FINAL_MESSAGE(x) for x in _results]
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
                        self.history.append(result)
                        if result.role == MessageRole.ASSISTANT:
                            self.on_end(result)
                            return Ok(result)
                except Exception:
                    self.scores[self.cursor].append(0.0)
            try:
                self._set_next_state()
            except Exception as e:
                _result = Err(e, str(e))
                self.on_error(_result)
                return _result
        e = Exception("The agent has reached the maximum number of turns.")
        _result = Err(e, "The agent has reached the maximum number of turns.")
        self.on_error(_result)
        return _result

    def _set_next_state(self) -> None:
        r"""Set the next state for the ToT agent based on the search method.

        Raises:
            Exception: If no valid state is found.
        """
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
                self._queue: List[Tuple[BaseMemory, int]] = []
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

    def add_tool(self, tool: Union["BaseAgent", BaseFunction]) -> Self:
        """Add a tool to the agent's toolset.

        Args:
            tool:
                The tool to add.

        Returns:
            The agent instance.
        """
        self.tools.append(tool)
        self.propose_model.config["tools"].append(tool.schema)
        return self

    def remove_tool(self, tool: Union["BaseAgent", BaseFunction]) -> Self:
        """Remove a tool from the agent's toolset.

        Args:
            tool:
                The tool to remove.

        Returns:
            The agent instance.
        """
        self.tools.remove(tool)
        self.propose_model.config["tools"].remove(tool.schema)
        return self

    def reset(self) -> Self:
        """Reset the agent's state.

        Returns:
            The agent instance.
        """
        self.history.clear()
        self.cursor = 0
        self.states = []
        self.scores = []
        self.visited = []
        return self
