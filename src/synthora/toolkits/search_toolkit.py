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

from synthora.toolkits import BaseToolkit
from synthora.toolkits.decorators import tool
from synthora.types.enums import Ok, Result
from synthora.workflows import BaseTask

from .search_toolkits import (
    search_arxiv,
    search_duckduckgo,
    search_google,
    search_wikipedia,
    search_youtube,
)


@tool
def search_all(query: str) -> Result[str, Exception]:
    r"""Search for a query in Wikipedia, Google, Arxiv, and Youtube.

    Args:
        query:
            The query to search for.
    """
    names = [
        "search_wikipedia",
        "search_google",
        "search_arxiv",
        "search_youtube",
        "search_duckduckgo",
    ]
    flow = (
        BaseTask(search_google.run)
        | BaseTask(search_wikipedia.run)
        | BaseTask(search_arxiv.run).s(5)
        | BaseTask(search_youtube.run).s(5)
        | BaseTask(search_duckduckgo.run).s("text", 5)
    )
    result = flow.run(query)
    ans = ""
    for name, res in zip(names, result):
        if res.is_ok:
            ans += f"{name}\n: {res.unwrap()}\n"
        else:
            ans += f"{name}\n: {res.unwrap_err()}\n"
    return Ok(ans)


class SearchToolkit(BaseToolkit):
    search_wikipedia = search_wikipedia
    search_google = search_google
    search_arxiv = search_arxiv
    search_youtube = search_youtube
    search_all = search_all
    search_duckduckgo = search_duckduckgo
