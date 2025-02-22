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
def search_file(dir_path: str, pattern: str) -> Result[str, Exception]:
    r"""Search for files in a directory.

    Args:
        dir_path:
            The directory path to search for files.
        pattern:
            The pattern to search for in the file names.

    """
    try:
        import os

        matches = []
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if pattern in file:
                    matches.append(os.path.join(root, file))
        if matches:
            return Ok("\n".join(matches))
        return Ok(f"No matches found for pattern {pattern} in {dir_path}")
    except Exception as e:
        return Err(e, str(e))
