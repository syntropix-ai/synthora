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

import re
from typing import Any, Set

from pydantic_core import core_schema
from pydantic_core.core_schema import StringSchema


class BasePrompt(str):
    """A base class for handling prompt templates that extends the built-in str
    class.

    This class provides functionality for template string formatting with
    argument validation.
    Inherits from str to maintain string-like behavior while adding
    prompt-specific features.
    """

    @property
    def args(self) -> Set[str]:
        """Extract all template arguments from the prompt string.

        Returns:
            A set of unique argument names found in the prompt template,
            extracted from patterns like {arg_name}.
        """
        return set(re.findall(r"{([^}]*)}", self))

    def format(self, **kwargs: Any) -> "BasePrompt":  # type: ignore[override]
        """Format the prompt template with provided arguments.

        Args:
            **kwargs:
                Keyword arguments to fill the template placeholders.
                Only arguments that exist in the template will be used.

        Returns:
            BasePrompt: A new BasePrompt instance with the template arguments
            replaced. Returns self if no template arguments exist.
        """
        if not self.args:
            return self
        return BasePrompt(
            self.format_map(
                {k: v for k, v in kwargs.items() if k in self.args}
            )
        )

    @classmethod
    def __get_pydantic_core_schema__(
        cls: Any, source: Any, handler: Any
    ) -> StringSchema:
        """Define the Pydantic core schema for BasePrompt serialization.

        Args:
            cls:
                The class being serialized.
            source:
                The source data.
            handler:
                The schema handler.

        Returns:
            A string schema for Pydantic serialization.
        """
        return core_schema.str_schema()
