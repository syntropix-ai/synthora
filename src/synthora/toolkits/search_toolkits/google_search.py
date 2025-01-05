# LICENSE HEADER MANAGED BY add-license-header
#
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
#


from googlesearch import search

from synthora.toolkits.decorators import tool
from synthora.types.enums import Err, Ok, Result


@tool
def google_search(query: str) -> Result[str, Exception]:
    r"""Search Google and return a list of URLs.

    Args:
        query (str): The search query to look up on Google

    Returns:
        Result[str, Exception]: A Result object containing either:
            - Ok(str): A list of URLs if successful
            - Err(Exception): An error with description if the search fails
    """
    try:
        return Ok("\n\n".join([str(item) for item in search(query, advanced=True)]))
    except Exception as e:
        return Err(e, f"Error: {e}\n Probably it is an invalid query.")