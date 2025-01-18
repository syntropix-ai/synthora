from typing import Optional

from synthora.toolkits.decorators import tool
from synthora.types.enums import Err, Ok, Result


@tool
def search_duckduckgo(
    query: str, source: str = "text", max_results: int = 5
) -> Result[str, Exception]:
    r"""Use DuckDuckGo search engine to search information for
    the given query.

    This function queries the DuckDuckGo API for related topics to
    the given search term. The results are formatted into a list of
    dictionaries, each representing a search result.

    Args:
        query (str): The query to be searched.
        source (str): The type of information to query (e.g., "text",
            "images", "videos"). Defaults to "text".
        max_results (int): Max number of results, defaults to `5`.
    """
    try:
        from duckduckgo_search import DDGS
        from requests.exceptions import RequestException

        ddgs = DDGS()
        ans = ""

        if source == "text":
            results = ddgs.text(keywords=query, max_results=max_results)
            for i, result in enumerate(results, start=1):
                ans += f"""
                Title: {result["title"]}
                Description: {result["body"]}
                URL: {result["href"]}
                """
        elif source == "images":
            results = ddgs.images(keywords=query, max_results=max_results)
            for i, result in enumerate(results, start=1):
                ans += f"""
                Title: {result["title"]}
                Image: {result["image"]}
                URL: {result["url"]}
                Source: {result["source"]}
                """

        elif source == "videos":
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
