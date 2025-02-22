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
def search_arxiv(
    query: str, max_results: Optional[int] = None
) -> Result[str, Exception]:
    r"""Search arXiv for papers based on the search terms.

    Args:
        query:
            The search terms to look up on arXiv.
        max_results:
            Maximum number of results to return. Defaults to None.
    """
    try:
        import arxiv

        client = arxiv.Client()
        search = arxiv.Search(query=query, max_results=max_results)

        results = client.results(search)
        return Ok(
            "\n".join(
                [
                    f"""
                    Entry ID: {result.entry_id}
                    Updated: {result.updated}
                    Published: {result.published}
                    Title: {result.title}
                    Authors: {result.authors}
                    Summary: {result.summary}
                    Journal Ref: {result.journal_ref}
                    DOI: {result.doi}
                    Primary Category: {result.primary_category}
                    Categories: {result.categories}
                    Links: {result.links}
                    PDF URL: {result.pdf_url}
                    """
                    for result in results
                ]
            )
        )
    except ImportError:
        raise ImportError(
            "Could not import arxiv. Please install it using "
            "`pip install arxiv`"
        )

    except Exception as e:
        return Err(e, f"Error: {e}")
