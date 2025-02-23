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


import json
import warnings
from copy import deepcopy
from typing import Any, Dict, List

from synthora.agents import VanillaAgent
from synthora.messages import user
from synthora.messages.base import BaseMessage
from synthora.utils.pydantic_model import get_pydantic_model
from synthora.workflows.base_task import BaseTask
from synthora.workflows.scheduler.process_pool import ProcessPoolScheduler


warnings.filterwarnings("ignore")

response_format = get_pydantic_model('{"score1": 0.0, "score2": 0.0}')


def score_response(
    history1: List[BaseMessage], history2: List[BaseMessage], prompt: str
) -> Dict[str, Any]:
    agent = VanillaAgent.default(
        f"You are a judger to score theses two responses. Please use score "
        f"from 0 to 10. The question is: {prompt}",
    )
    agent.model.config["response_format"] = response_format
    openai_history1 = [msg.to_openai_message() for msg in history1[1:]]
    openai_history2 = [msg.to_openai_message() for msg in history2[1:]]
    _history1 = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in openai_history1]
    )
    _history2 = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in openai_history2]
    )

    agent.history.append(user(f"Response 1:\n{_history1}"))
    agent.history.append(user(f"Response 2:\n{_history2}"))
    resp = agent.run("Please score the two responses.").unwrap().parsed
    result = {
        "chosen": openai_history1
        if resp.score1 > resp.score2
        else openai_history2,
        "rejected": openai_history2
        if resp.score1 > resp.score2
        else openai_history1,
        "score_chosen": resp.score1
        if resp.score1 > resp.score2
        else resp.score2,
        "score_rejected": resp.score2
        if resp.score1 > resp.score2
        else resp.score1,
    }
    print(resp)
    return result


def generate_data(system1: str, system2: str, prompt: str) -> Dict[str, Any]:
    agent1, agent2 = (
        VanillaAgent.default(system1),
        VanillaAgent.default(system2),
    )
    flow = (BaseTask(agent1.run) | BaseTask(agent2.run)).s(prompt)
    _ = flow.run()
    return score_response(agent1.history, agent2.history, prompt)


if __name__ == "__main__":
    system_message = "You are an AI Assistant."
    with open("examples/workflows/data/questions.jsonl", "r") as f:
        prompts = [json.loads(line)["turns"][0] for line in f.readlines()]

    # prompts = prompts[:1]
    system1 = [system_message for _ in range(len(prompts))]
    system2 = deepcopy(system1)

    flow = ProcessPoolScheduler.starmap(
        BaseTask(generate_data), zip(system1, system2, prompts)
    )
    results = flow.run()

    with open("examples/workflows/data/results.jsonl", "w") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")
