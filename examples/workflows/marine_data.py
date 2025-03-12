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


import warnings
from typing import Dict, List

from synthora.agents import VanillaAgent
from synthora.messages.base import BaseMessage
from synthora.workflows import task
from synthora.workflows.scheduler.thread_pool import ThreadPoolScheduler
from synthora.toolkits.search_toolkits import search_wikipedia
from pydantic import BaseModel
import json


warnings.filterwarnings("ignore")

class MarineDataItem(BaseModel):
    question: str
    answer: str

class MarineData(BaseModel):
    items: List[MarineDataItem]

@task
def search_wikipedia_task(query: str) -> str:
    try:
        return search_wikipedia.run(query).unwrap()
    except Exception as e:
        return str(e)

@task
def generate_data(doc: str) -> List[BaseMessage]:
    agent = VanillaAgent.default("You are a marine data expert. You are given a document and you need to generate several questions and answers about the document.")
    agent.model.config["response_format"] = MarineData
    results = agent.run(doc).unwrap().parsed
    return results



@task
def convert(resps: List[MarineData]) -> List[Dict[str, str]]:
    data = []
    for resp in resps:
        data.extend(resp.items)
    
    return list(map(lambda x: x.model_dump(), data))


concepts = [
    "Acoustic seabed classification",
    "Advection",
    # "Ageostrophy",
    # "Baroclinity",
    # "Coriolis frequency"
]


flow = ThreadPoolScheduler.map(search_wikipedia_task >> generate_data, concepts) >> convert


data = flow.run()

with open("marine_data.json", "w") as f:
    json.dump(data, f, indent=4)

for d in data:
    print(d)
    print("=" * 30)
