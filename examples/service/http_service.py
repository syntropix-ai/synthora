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


import json
import time
import warnings

from synthora.agents import ReactAgent
from synthora.callbacks import RichOutputHandler
from synthora.configs import AgentConfig
from synthora.services.http_service import HttpService
from synthora.tracers import SimpleTracer


warnings.filterwarnings("ignore")

config = AgentConfig.from_file("examples/agents/configs/react_agent.yaml")


agent = ReactAgent.from_config(config)

http_service = HttpService()
http_service.add(agent)
http_service.run(host="0.0.0.0", port=8000)
time.sleep(10)
http_service.stop()
