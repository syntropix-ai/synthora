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
from typing import IO, Any

import yaml


class YAMLLoader(yaml.SafeLoader):
    def __init__(self, stream: IO[Any]) -> None:
        """
        Initializes a new instance of the Loader class.
        :param stream: The stream to load YAML from.
        :type stream: IOBase
        """
        self._root = Path(stream.name).resolve().parent
        super(YAMLLoader, self).__init__(stream)
        self.add_constructor("!include", YAMLLoader.include)
        self.add_constructor("!file", YAMLLoader.file)

    def include(self, node: yaml.Node) -> Any:
        filename = Path(self.construct_scalar(node))
        if not filename.is_absolute():
            filename = self._root / filename
        with open(filename, "r") as f:
            return yaml.load(f, YAMLLoader)

    def file(self, node: yaml.Node) -> Any:
        filename = Path(self.construct_scalar(node))
        if not filename.is_absolute():
            filename = self._root / filename
        with open(filename, "r") as f:
            return f.read().strip()
