from urllib.parse import urlparse
import base64
from pathlib import Path
import mimetypes

def parse_image(path: str) -> str:
    if is_url(path):
        return path
    if path.startswith("data:"):
        return path
    return image2base64(path)

def is_url(path: str) -> bool:
    return urlparse(path).scheme in ['http', 'https']


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

