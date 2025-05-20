from copy import deepcopy
from typing import List

from synthora.code_automations.agents.agents import create_code_generation_agent
from synthora.code_automations.blocks.base import BaseAutomationBlock
from synthora.types.enums import AutomationBlockType, Err, Result


class AutomationGraph:
    def __init__(self, description: str, blocks: List[BaseAutomationBlock]):
        self.description = description
        self.leveled_blocks = AutomationGraph.compile(blocks)
        
    def __str__(self):
        return "\n".join([", ".join([str(block) for block in level]) for level in self.leveled_blocks])
    
    def __repr__(self):
        return self.__str__()
    
    def run(self) -> Result[str, Exception]:
        try:
            for level in self.leveled_blocks:
                for block in level:
                    block.run()
            agent = create_code_generation_agent()
            blocks = [block for level in self.leveled_blocks for block in level]
            result = agent.run("", description=self.description, code="\n".join([block.full_str() for block in blocks]))
            if result.is_err:
                return result
            return result.unwrap().parsed.code
        except Exception as e:
            return Err(e, str(e))
        
    async def async_run(self) -> Result[str, Exception]:
        try:
            for level in self.leveled_blocks:
                for block in level:
                    await block.run_async()
            agent = create_code_generation_agent()
            blocks = [block for level in self.leveled_blocks for block in level]
            result = await agent.async_run("", description=self.description, code="\n".join([block.full_str() for block in blocks]))
            if result.is_err:
                return result
            return result.unwrap().parsed.code
        except Exception as e:
            return Err(e, str(e))
    
    @staticmethod
    def compile(blocks: List[BaseAutomationBlock]) -> List[List[BaseAutomationBlock]]:
        stack = [block for block in blocks if len(block.dependencies) == 0]
        if not stack:
            raise ValueError("No starting blocks found")
        inp_degrees = {b: len(b.dependencies) for b in blocks}
        result = [stack]
        
        while stack:
            new_stack = []
            
            for s in stack:
                for o in s.dependents:
                    inp_degrees[o] -= 1
                    if inp_degrees[o] == 0:
                        new_stack.append(o)
            
            stack = new_stack
            result.append(stack)
        
        if sum(inp_degrees.values()) != 0:
            raise ValueError("Cycle detected")
        
        return result
    

        
        