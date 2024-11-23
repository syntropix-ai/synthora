# LICENSE HEADER MANAGED BY add-license-header
#
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
# MIT License
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
#

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Self, Type, Union

from syntropic.models.base import BaseModelBackend


class BaseConfig(ABC):
    def __init__(
        self, name: str, model: Union[BaseModelBackend, Dict[str, BaseModelBackend]]
    ):
        self.name = name
        self.model = model

    @classmethod
    def load(cls: Type[Self], source: Union[Path, str]) -> Self:
        assert isinstance(source, (str, Path)), f"Invalid source type {type(source)}"
        file_path = Path(source) if isinstance(source, str) else source
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} not found")
        if not file_path.is_file():
            raise ValueError(f"{file_path} is not a file")
        return cls.from_file(file_path)

    @abstractmethod
    @classmethod
    def from_file(cls: Type[Self], path: Path) -> Self: ...
