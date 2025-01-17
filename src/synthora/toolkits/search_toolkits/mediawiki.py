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

from typing import Optional
from synthora.toolkits.base import BaseToolkit
from synthora.toolkits.decorators import tool
from synthora.types.enums import Err, Ok, Result


class MediawikiToolkit(BaseToolkit):
    def __init__(self, url: Optional[str] = None):
        super().__init__()
        try:
            from mediawiki import MediaWiki
            from mediawiki.exceptions import DisambiguationError, PageError
            self.mediawiki = MediaWiki(url=url) if url else MediaWiki()
        except ImportError:
            raise ImportError(
                "Could not import mediawiki. Please install it using "
                "`pip install pymediawiki`"
            )

    @tool
    def search_mediawiki(
        self, query: str, sentences: int = 5, auto_suggest: bool = False
    ) -> Result[str, Exception]:
        """Search Mediawiki and return a summary of the article.

        This function attempts to find and summarize a Mediawiki article based on
        the query. If the query is ambiguous, it returns the summary of the first
        suggested option.

        Args:
            query:
                The search query to look up on Mediawiki.
            sentences:
                Number of sentences to return in the summary. Defaults to 5.
            auto_suggest:
                Whether to auto-suggest similar article titles. Defaults to False.

        Returns:
            Result[str, Exception]: A Result object containing either:
                - Ok(str): The article summary if successful
                - Err(Exception): An error with description if the search fails

        Raises:
            ImportError: If the mediawiki package is not installed

        Examples:
            >>> result = search_mediawiki("Python programming")
            >>> if result.is_ok:
            ...     print(result.unwrap())
            ... else:
            ...     print(f"Error: {result.unwrap_err()}")

        Note:
            - Handles DisambiguationError by choosing the first suggested option
            - Handles PageError by returning an error message suggesting to try
                another query
            - Requires the 'mediawiki' package to be installed
        """

        try:
            from mediawiki.exceptions import DisambiguationError

            return Ok(
                self.mediawiki.summary(query, sentences=sentences, auto_suggest=auto_suggest)
            )
        except DisambiguationError as e:
            return Ok(
                self.mediawiki.summary(
                    e.options[0], sentences=sentences, auto_suggest=auto_suggest
                )
            )
        except Exception as e:
            return Err(e, f"An exception occurred during the search: {e}")
