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
def search_duckduckgo(
    query: str, content_type: str = "text", max_results: int = 5
) -> Result[str, Exception]:
    r"""Use DuckDuckGo search engine to search information for
    the given query.

    This function queries the DuckDuckGo API for related topics to
    the given search term. The results are formatted into a list of
    dictionaries, each representing a search result.

    Args:
        query (str): The query to be searched.
        content_type (str): The type of information to query (e.g., "text",
            "images", "videos"). Defaults to "text".
        max_results (int): Max number of results, defaults to `5`.
    """
    try:
        from duckduckgo_search import DDGS
        from requests.exceptions import RequestException

        ddgs = DDGS()
        ans = ""

        if content_type == "text":
            results = ddgs.text(keywords=query, max_results=max_results)
            for i, result in enumerate(results, start=1):
                ans += f"""
                Title: {result["title"]}
                Description: {result["body"]}
                URL: {result["href"]}
                """
        elif content_type == "images":
            results = ddgs.images(keywords=query, max_results=max_results)
            for i, result in enumerate(results, start=1):
                ans += f"""
                Title: {result["title"]}
                Image: {result["image"]}
                URL: {result["url"]}
                Source: {result["source"]}
                """

        elif content_type == "videos":
            results = ddgs.videos(keywords=query, max_results=max_results)
            for i, result in enumerate(results, start=1):
                ans += f"""
                Title: {result["title"]}
                Description: {result["description"]}
                Embed URL: {result["embed_url"]}
                Publisher: {result["publisher"]}
                Duration: {result["duration"]}
                Published: {result["published"]}
                """
        return Ok(ans)
    except ImportError:
        raise ImportError(
            "Could not import duckduckgo_search. Please install it using "
            "`pip install duckduckgo_search`"
        )
    except RequestException as e:
        return Err(e, f"Error: {e}")
