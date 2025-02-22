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
def move_file(src: str, dest: str) -> Result[str, Exception]:
    r"""Move a file from source to destination.

    Args:
        src:
            The source file path.
        dest:
            The destination file path.
    """
    try:
        import shutil

        shutil.move(src, dest)
        return Ok(f"File moved successfully from {src} to {dest}")
    except Exception as e:
        return Err(e, str(e))
