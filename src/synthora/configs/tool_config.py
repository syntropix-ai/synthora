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

from pathlib import Path
from typing import Any, Dict, List, Optional, Self, Type, Union

import yaml

from synthora.configs.base import BaseConfig
from synthora.utils import YAMLLoader


class ToolConfig(BaseConfig):
    """Configuration class for agent tools/plugins

    Attributes:
        target (str): Target identifier or path for the tool
        trace (Optional[bool]): Whether to enable tracing for this tool, defaults to True
        args (Optional[Dict[str, Any]]): Optional arguments for tool initialization
    """

    target: str
    trace: Optional[bool] = True
    args: Optional[Dict[str, Any]] = None

    @classmethod
    def from_file(cls: Type[Self], path: Path) -> Self:
        """Load tool configuration from a YAML file

        Args:
            path (Path): Path to the YAML configuration file

        Returns:
            Self: Instance of ToolConfig

        Raises:
            ValueError: If YAML file cannot be loaded properly
        """
        try:
            with open(path, "r") as file:
                data = yaml.load(file, YAMLLoader)
        except yaml.YAMLError as e:
            raise ValueError(f"Error loading yaml file {path}: {e}")
        return cls(**data)

    @classmethod
    def from_dict(cls: Type[Self], data: Dict[str, Any]) -> Self:
        """Create tool configuration from a dictionary

        Args:
            data (Dict[str, Any]): Dictionary containing tool configuration

        Returns:
            Self: Instance of ToolConfig
        """
        return cls(**data)

    @staticmethod
    def parse_tools(plugins: List[Union[str, Dict[str, Any]]]) -> List["ToolConfig"]:
        """Parse a list of tool configurations from mixed format input

        Args:
            plugins (List[Union[str, Dict[str, Any]]]): List of tool configurations,
                each item can be either:
                - str: Simple tool target identifier
                - Dict: Full tool configuration dictionary

        Returns:
            List[ToolConfig]: List of parsed ToolConfig instances

        Example:
            >>> tools = ['tool1', {'target': 'tool2', 'args': {'param': 'value'}}]
            >>> parsed = ToolConfig.parse_tools(tools)
        """
        parsed_plugins = []
        for plugin in plugins:
            if isinstance(plugin, str):
                parsed_plugins.append(ToolConfig(target=plugin, args={}))
            else:
                parsed_plugins.append(ToolConfig(**plugin))
        return parsed_plugins
