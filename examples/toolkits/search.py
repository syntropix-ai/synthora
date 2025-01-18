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

import json
from synthora.agents import VanillaAgent
from synthora.callbacks import RichOutputHandler
from synthora.toolkits.search_toolkit import search_all
from synthora.toolkits.file_toolkit import FileToolkit

write_file = FileToolkit.write_file
list_directory = FileToolkit.list_directory
agent = VanillaAgent.default(
    tools=[search_all, write_file, list_directory], handlers=[RichOutputHandler()]
)

while True:
    inp = input("Enter a search query: ")
    if inp == "exit":
        break
    res = agent.run(inp)
    
