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

from synthora.toolkits.decorators import tool
from synthora.types.enums import Err, Ok, Result


@tool
def search_wikipedia(
    query: str, sentences: int = 15, auto_suggest: bool = False
) -> Result[str, Exception]:
    """Search Wikipedia and return a summary of the article.

    This function attempts to find and summarize a Wikipedia article based on
    the query. If the query is ambiguous, it returns the summary of the first
    suggested option.

    Args:
        query:
            The search query to look up on Wikipedia.
        sentences:
            Number of sentences to return in the summary. Defaults to 5.
        auto_suggest:
            Whether to auto-suggest similar article titles. Defaults to False.

    Returns:
        Result[str, Exception]: A Result object containing either:
            - Ok(str): The article summary if successful
            - Err(Exception): An error with description if the search fails

    Raises:
        ImportError: If the wikipedia package is not installed

    Examples:
        >>> result = search_wikipedia("Python programming")
        >>> if result.is_ok:
        ...     print(result.unwrap())
        ... else:
        ...     print(f"Error: {result.unwrap_err()}")

    Note:
        - Handles DisambiguationError by choosing the first suggested option
        - Handles PageError by returning an error message suggesting to try
            another query
        - Requires the 'wikipedia' package to be installed
    """
    try:
        import wikipedia
    except ImportError:
        raise ImportError(
            "Could not import wikipedia. Please install it using "
            "`pip install wikipedia`"
        )

    try:
        return Ok(
            wikipedia.summary(
                query, sentences=sentences, auto_suggest=auto_suggest
            )
        )
    except wikipedia.exceptions.DisambiguationError as e:
        return Ok(
            wikipedia.summary(
                e.options[0], sentences=sentences, auto_suggest=auto_suggest
            )
        )
    except wikipedia.exceptions.PageError as e:
        return Err(e, str(e) + " Please try another query.")
    except Exception as e:
        return Err(e, f"An exception occurred during the search: {e}")
