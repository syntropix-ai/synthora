from typing import List, Optional
from synthora.code_automations.blocks.base import BaseAutomationBlock
from synthora.types.enums import AutomationBlockType

class InputBlock(BaseAutomationBlock):
    def __init__(self, name: str, description: str, code: Optional[str] = None, extra_dependencies: Optional[List["BaseAutomationBlock"]] = None):
        super().__init__(name, description, AutomationBlockType.INPUT, code, extra_dependencies)
