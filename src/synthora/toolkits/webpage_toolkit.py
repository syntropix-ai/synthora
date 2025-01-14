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

from trafilatura import extract, fetch_url, html2txt

from synthora.toolkits.base import BaseToolkit
from synthora.toolkits.decorators import tool


class TrafilaturaWebpageReader(BaseToolkit):
    """Toolkit for extracting the main content from a webpage using the
    trafilatura library.
    """

    def __init__(self, full_text: bool = False):
        self.full_text = full_text
        super().__init__()

    @tool
    def trafilatura_webpage_reader(self, url: str) -> str:
        """Extracts the main content from a webpage using the trafilatura
        library.

        Args:
            url (str): The URL of the webpage to read.

        Returns:
            str: The main content of the webpage.
        """
        html = fetch_url(url)
        text = extract(html) if not self.full_text else html2txt(html)
        return str(text)
