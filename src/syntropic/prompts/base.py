import re
from typing import Any, Set

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class BasePrompt(str):
    @property
    def args(self) -> Set[str]:
        return set(re.findall(r"{([^}]*)}", self))

    def format(self, **kwargs: Any) -> "BasePrompt":
        return BasePrompt(
            self.format_map({k: v for k, v in kwargs.items() if k in self.args})
        )

    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        return core_schema.str_schema()
