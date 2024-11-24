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

from synthora.toolkits.decorators import tool
from synthora.types.enums import Err, Ok, Result


@tool
def search_wikipedia(
    query: str, sentences: int = 5, auto_suggest: bool = False
) -> Result[str, Exception]:
    try:
        import wikipedia  # type: ignore[import-not-found]
    except ImportError:
        raise ImportError(
            "Could not import wikipedia. Please install it using `pip install wikipedia`"
        )

    try:
        return Ok(
            wikipedia.summary(query, sentences=sentences, auto_suggest=auto_suggest)
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
