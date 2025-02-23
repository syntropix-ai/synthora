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

from pathlib import Path
from typing import Any, Dict, Type, Union


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from pydantic import BaseModel


class BaseConfig(BaseModel):
    """Base configuration class that provides common loading functionality

    All configuration classes should inherit from this base class.
    """

    @classmethod
    def load(
        cls: Type[Self], source: Union[Path, str, Dict[str, Any]]
    ) -> Self:
        """Universal loader that handles different input types

        Args:
            source (Union[Path, str, Dict[str, Any]]): Configuration source,
            can be:
                - Path object pointing to config file
                - String path to config file
                - Dictionary containing config data

        Returns:
            Self: Instance of the configuration class

        Raises:
            AssertionError: If source type is invalid
            FileNotFoundError: If specified file path doesn't exist
            ValueError: If specified path is not a file
        """
        assert isinstance(
            source, (str, Path, dict)
        ), f"Invalid source type {type(source)}"
        if isinstance(source, dict):
            return cls.from_dict(source)
        file_path = Path(source) if isinstance(source, str) else source
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} not found")
        if not file_path.is_file():
            raise ValueError(f"{file_path} is not a file")
        return cls.from_file(file_path)

    @classmethod
    def from_file(cls: Type[Self], path: Path) -> Self:
        """Load configuration from a file

        Args:
            path (Path): Path to the configuration file

        Returns:
            Self: Instance of the configuration class

        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        raise NotImplementedError

    @classmethod
    def from_dict(cls: Type[Self], data: Dict[str, Any]) -> Self:
        """Create configuration from a dictionary

        Args:
            data (Dict[str, Any]): Dictionary containing configuration data

        Returns:
            Self: Instance of the configuration class

        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        raise NotImplementedError
