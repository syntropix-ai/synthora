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
        