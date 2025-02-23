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

import pytest

from synthora.prompts import BasePrompt


class TestPrompts:
    def test_from_str(self):
        prompt = BasePrompt("Hello World!")
        assert prompt == "Hello World!"
        assert prompt.args == set()

    def test_format(self):
        prompt = BasePrompt("Hello {name}!")
        formatted = prompt.format(name="World")
        assert formatted == "Hello World!"
        assert formatted.args == set()

    def test_format_missing_args(self):
        prompt = BasePrompt("Hello {name}!")
        assert prompt == "Hello {name}!"
        assert prompt.args == {"name"}
        with pytest.raises(KeyError):
            prompt.format()

    def test_format_extra_args(self):
        prompt = BasePrompt("Hello {name}!")
        formatted = prompt.format(name="World", extra="Extra")
        assert formatted == "Hello World!"

    def test_multiple_args(self):
        prompt = BasePrompt("Hello {name}! My name is {self_name}.")
        assert prompt.args == {"name", "self_name"}
        formatted = prompt.format(name="World", self_name="Synthora")
        assert formatted == "Hello World! My name is Synthora."
