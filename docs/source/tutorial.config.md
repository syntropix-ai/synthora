<!-- LICENSE HEADER MANAGED BY add-license-header

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
-->

# Create Agent from Config File

### vanilla_agent.yaml

```yaml
name: test
type: vanilla
model: !include basic_model.yaml
prompt: "You are an AI Assistant. You are here to help me with my queries."
tools:
  - synthora.toolkits.SearchToolkit
```

### basic_model.yaml
```yaml
name: searcher
model_type: gpt-4o
backend: openai_chat
backend_config:
  api_key: "your-api-key"
config:
  temperature: 0
  top_p: 1.0
  stream: true
```
### Code
```python

from synthora.agents import VanillaAgent
from synthora.configs import AgentConfig
from synthora.callbacks import RichOutputHandler

import warnings
warnings.filterwarnings("ignore")

config = AgentConfig.from_file("examples/agents/configs/vanilla_agent.yaml")

agent = VanillaAgent.from_config(config)
handler = RichOutputHandler()
agent.tools[0].callback_manager.add(handler)
agent.model.callback_manager.add(handler)
agent.callback_manager.add(handler)

agent.run("Search Trump on Wikipedia")
```
