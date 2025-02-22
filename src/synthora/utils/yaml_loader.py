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
from typing import IO, Any

import yaml

from synthora.prompts import buildin


class YAMLLoader(yaml.SafeLoader):
    def __init__(self, stream: IO[Any]) -> None:
        """
        Initialize a custom YAML loader with support for !include and !file
        directives.

        Args:
            stream:
                An input stream object containing YAML content.
                Must have a 'name' attribute pointing to the source file.
        """
        self._root = Path(stream.name).resolve().parent
        super(YAMLLoader, self).__init__(stream)
        self.add_constructor("!include", YAMLLoader.include)
        self.add_constructor("!file", YAMLLoader.file)
        self.add_constructor("!prompt", YAMLLoader.prompt)

    def include(self, node: yaml.Node) -> Any:
        """
        Process !include directive to include and parse another YAML file.

        Args:
            node:
                YAML node containing the path to the file to include.

        Returns:
            The parsed content of the included YAML file.
        """
        filename = Path(self.construct_scalar(node))
        if not filename.is_absolute():
            filename = self._root / filename
        with open(filename, "r") as f:
            return yaml.load(f, YAMLLoader)

    def file(self, node: yaml.Node) -> Any:
        """
        Process !file directive to read raw content from another file.

        Args:
            node:
                YAML node containing the path to the file to read.

        Returns:
            The raw content of the file as a string, with leading/trailing
            whitespace removed.
        """
        filename = Path(self.construct_scalar(node))
        if not filename.is_absolute():
            filename = self._root / filename
        with open(filename, "r") as f:
            return f.read().strip()

    def prompt(self, node: yaml.Node) -> Any:
        """
        Process !prompt directive to read user input from the console.

        Args:
            node:
                YAML node containing the prompt message.

        Returns:
            The user input as a string.
        """
        name = self.construct_scalar(node)
        prompt_message = getattr(buildin, name)
        return prompt_message
