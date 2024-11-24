import importlib
from pathlib import Path
from typing import Any, IO
import yaml
import os


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
