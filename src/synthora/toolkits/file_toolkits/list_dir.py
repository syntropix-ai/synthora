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


from synthora.toolkits.decorators import tool
from synthora.types.enums import Err, Ok, Result


@tool
def list_directory(path: str) -> Result[str, Exception]:
    r"""List the contents of a directory.

    Args:
        path:
            The directory path to list the contents of.

    """
    try:
        import os

        items = os.listdir(path)
        if not items:
            return Ok(f"No items found in {path}")
        return Ok("\n".join(os.listdir(path)))
    except Exception as e:
        return Err(e, str(e))