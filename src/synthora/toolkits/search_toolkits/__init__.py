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

from .arxiv import search_arxiv
from .ddgo import search_duckduckgo
from .google_search import search_google
from .mediawiki import MediawikiToolkit
from .wikipidia import search_wikipedia
from .youtube import search_youtube


__all__ = [
    "search_wikipedia",
    "search_google",
    "MediawikiToolkit",
    "search_youtube",
    "search_arxiv",
    "search_duckduckgo",
]
