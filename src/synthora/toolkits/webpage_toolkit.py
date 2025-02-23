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

import requests
from bs4 import BeautifulSoup
from trafilatura import extract, fetch_url, html2txt

from synthora.toolkits.base import BaseToolkit
from synthora.toolkits.decorators import tool
from synthora.types.enums import Err, Ok, Result


@tool
def get_webpage(url: str) -> Result[str, Exception]:
    r"""Retrieve the text content of a web page.

    Args:
        url (str): The URL of the web page to retrieve.

    Returns:
        Result[str, Exception]: A Result object containing either:
            - Ok(str): The text content of the web page if successful
            - Err(Exception): An error with description if the retrieval fails
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        text = " ".join(line for line in lines if line)[:4096] + "..."
        return Ok(text)
    except Exception as e:
        return Err(e, f"Error: {e}\n Probably it is an invalid URL.")


class TrafilaturaWebpageReader(BaseToolkit):
    """Toolkit for extracting the main content from a webpage using the
    trafilatura library.
    """

    get_webpage = get_webpage

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
