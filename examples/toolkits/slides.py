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

import dotenv

from synthora.agents import VanillaAgent
from synthora.callbacks import RichOutputHandler
from synthora.toolkits.search_toolkit import SearchToolkit
from synthora.toolkits.webpage_toolkit import TrafilaturaWebpageReader
from synthora.toolkits.slides import SlidesToolkit


toolkit = SearchToolkit()

dotenv.load_dotenv()


agent = VanillaAgent.default(
    tools=SlidesToolkit().sync_tools + [*TrafilaturaWebpageReader(full_text=True).sync_tools],  # type: ignore[arg-type]
    handlers=[RichOutputHandler()],
)

agent.run("generate a PPT about https://ai4ocean.xyz, including Products, Team, Research, Projects, Publications, Education, Partnership, etc. You can only use the content from the webpage.")
