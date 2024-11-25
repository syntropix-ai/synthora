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

import base64
import mimetypes
from pathlib import Path
from urllib.parse import urlparse


def parse_image(path: str) -> str:
    if is_url(path):
        return path
    if path.startswith("data:"):
        return path
    return image2base64(path)


def is_url(path: str) -> bool:
    return urlparse(path).scheme in ["http", "https"]


def image2base64(path: str) -> str:
    if not Path(path).is_file():
        raise FileNotFoundError(f"The file at path {path} does not exist.")
    mime_type, _ = mimetypes.guess_type(path)
    with open(path, "rb") as image_file:
        base64_encoded = base64.b64encode(image_file.read()).decode("utf-8")
    base64_encoded = f"base64,{base64_encoded}"
    if mime_type:
        base64_encoded = f"data:{mime_type};{base64_encoded}"
    return base64_encoded
