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

from typing import Optional

from synthora.toolkits.decorators import tool
from synthora.types.enums import Err, Ok, Result


@tool
def search_youtube(
    query: str, max_results: Optional[int] = None
) -> Result[str, Exception]:
    r"""Search YouTube for videos based on the search terms.

    Args:
        query:
            The search terms to look up on YouTube.
        max_results:
            Maximum number of results to return. Defaults to None.
    """
    try:
        from youtube_search import YoutubeSearch

        resp = YoutubeSearch(query, max_results).to_dict()
        return Ok(
            "\n".join(
                [
                    f"""
                    Title: {video["title"]}
                    Description: {video["long_desc"]}
                    Channel: {video["channel"]}
                    Duration: {video["duration"]}
                    Views: {video["views"]}
                    Publish Time: {video["publish_time"]}
                    URL: {"https://www.youtube.com"  + video["url_suffix"]}
                    """
                    for video in resp
                ]
            )
        )
    except ImportError:
        raise ImportError(
            "Could not import youtube_search. Please install it using "
            "`pip install youtube_search`"
        )
    except Exception as e:
        return Err(e, f"Error: {e}")
