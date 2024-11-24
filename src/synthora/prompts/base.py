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

import re
from typing import Any, Set

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