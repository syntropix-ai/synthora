# LICENSE HEADER MANAGED BY add-license-header
#
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
#


import asyncio
import json
import warnings
from synthora.tracers import SimpleTracer
from synthora.agents import ReactAgent
from synthora.callbacks import RichOutputHandler
from synthora.configs import AgentConfig
import fastapi
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import json
import warnings
from synthora.tracers import SimpleTracer
from synthora.agents import ReactAgent
from synthora.callbacks import RichOutputHandler
from synthora.configs import AgentConfig


warnings.filterwarnings("ignore")

config = AgentConfig.from_file("examples/agents/configs/react_agent.yaml")
from fastapi import BackgroundTasks

tracer = SimpleTracer()
@app.get("/")
async def read_root(background_tasks: BackgroundTasks):
    # with open("result.json", "r") as f:
    #     data = json.load(f)
    global tracer
    agent = ReactAgent.from_config(config)
    handler = RichOutputHandler()
    agent.add_handler(handler)

    
    tracer.trace(agent)
    tracer.reset()


    asyncio.create_task(agent.async_run("Search Openai on Wikipedia. Output Your thought first!"))

    async def stream():
        while True:
            if tracer.events:
                item = tracer.events.pop(0).to_dict()
                print(item)
                yield f"data: {json.dumps(item)}\n\n"
                if item["event_type"] == "on_agent_end":
                    break
            await asyncio.sleep(0.1)
    return StreamingResponse(stream(), media_type="text/event-stream")

