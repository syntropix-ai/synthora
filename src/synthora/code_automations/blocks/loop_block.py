from typing import List, Optional
from synthora.code_automations.blocks.base import BaseAutomationBlock
from synthora.types.enums import AutomationBlockType

class LoopBlock(BaseAutomationBlock):
    def __init__(self, name: str, description: str, parallel_size: int = 1, code: Optional[str] = None, extra_dependencies: Optional[List["BaseAutomationBlock"]] = None):
        super().__init__(name, description, AutomationBlockType.LOOP, code, extra_dependencies)
        if parallel_size <= 0:
            raise ValueError("Parallel size must be greater than 0")
        self.parallel_size = parallel_size
