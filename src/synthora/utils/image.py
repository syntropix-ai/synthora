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

import base64
import mimetypes
from pathlib import Path
from urllib.parse import urlparse


def parse_image(path: str) -> str:
    """Parse an image path and convert it to an appropriate format.

    This function handles different types of image inputs:
    - URLs (http/https)
    - Data URIs (data:...)
    - Local file paths (converts to base64)

    Args:
        path (str): The image path, URL, or data URI

    Returns:
        str: The processed image string:
            - Original URL for http/https URLs
            - Original string for data URIs
            - Base64 encoded string for local files

    Example:
        >>> parse_image("https://example.com/image.jpg")
        'https://example.com/image.jpg'
        >>> parse_image("/path/to/local/image.jpg")
        'data:image/jpeg;base64,/9j/4AAQSkZJRg...'
    """
    if is_url(path):
        return path
    if path.startswith("data:"):
        return path
    return image2base64(path)


def is_url(path: str) -> bool:
    """Check if a given path is a valid HTTP/HTTPS URL.

    Args:
        path (str): The path to check

    Returns:
        bool: True if path is an HTTP/HTTPS URL, False otherwise

    Example:
        >>> is_url("https://example.com/image.jpg")
        True
        >>> is_url("/local/path/image.jpg")
        False
    """
    return urlparse(path).scheme in ["http", "https"]


def image2base64(path: str) -> str:
    """Convert a local image file to a base64 encoded data URI.

    Args:
        path (str): Path to the local image file

    Returns:
        str: Base64 encoded data URI string in format:
            'data:<mime_type>;base64,<encoded_data>'

    Raises:
        FileNotFoundError: If the specified file does not exist

    Example:
        >>> image2base64("image.jpg")
        'data:image/jpeg;base64,/9j/4AAQSkZJRg...'
    """
    # Verify file exists
    if not Path(path).is_file():
        raise FileNotFoundError(f"The file at path {path} does not exist.")
    mime_type, _ = mimetypes.guess_type(path)

    # Read and encode the image file
    with open(path, "rb") as image_file:
        base64_encoded = base64.b64encode(image_file.read()).decode("utf-8")

    # Format the base64 string
    base64_encoded = f"base64,{base64_encoded}"

    # Add MIME type if available
    if mime_type:
        base64_encoded = f"data:{mime_type};{base64_encoded}"

    return base64_encoded
