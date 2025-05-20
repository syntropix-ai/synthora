from abc import ABC, abstractmethod
import json
from typing import Any, List, Optional

from synthora.code_automations.agents.agents import create_code_block_generation_agent
from synthora.types.enums import AutomationBlockType, Result

from pydantic import BaseModel


    
class BaseAutomationBlock(ABC):
    def __init__(self, name: str, description: str, block_type: AutomationBlockType, code: Optional[str] = None, extra_dependencies: Optional[List["BaseAutomationBlock"]] = None):
        self.name = name
        self.description = description
        self.block_type = block_type
        self.code = code
        self.extra_dependencies = extra_dependencies or []
        self.extra_dependent = []
        for dep in self.extra_dependencies:
            dep.extra_dependent.append(self)
        
        self.ins = set([])
        self.outs = set([])
        
    def __hash__(self):
        return hash(self.name + self.block_type)
    
    def __eq__(self, other):
        return self.name == other.name and self.block_type == other.block_type
    
    def __str__(self):
        return f"{self.name} ({self.block_type})"
    
    def __repr__(self):
        return f"{self.name} ({self.block_type})"
    
    def full_str(self):
        return f"""
            {self.name} ({self.block_type})
            {self.description}

            Code:
            {self.code}
            """
    
    def __rshift__(self, other: "BaseAutomationBlock"):
        if other.block_type == AutomationBlockType.INPUT:
            raise ValueError("Input block cannot be a dependency")
        
        self.outs.add(other)
        other.ins.add(self)
        
        return other
    
    def __lshift__(self, other: "BaseAutomationBlock"):
        if self.block_type == AutomationBlockType.INPUT:
            raise ValueError("Input block cannot be a dependency")
        
        self.ins.add(other)
        other.outs.add(self)
    
    @property
    def dependencies(self) -> List["BaseAutomationBlock"]:
        return list(set(list(self.ins) + self.extra_dependencies))
    
    @property
    def dependents(self) -> List["BaseAutomationBlock"]:
        return list(set(self.extra_dependent + list(self.outs)))
    
    @property
    def all_dependencies(self) -> List["BaseAutomationBlock"]:
        return list(set(self.dependencies + self.dependents))
    
    # @abstractmethod
    def run(self) -> Result[Any, Exception]:
        agent = create_code_block_generation_agent()
        
        result = agent.run("", description=self.description, dependencies="\n".join([dep.full_str() for dep in self.dependencies]), dependents="\n".join([dep.full_str() for dep in self.dependents]))
        code_result = result.unwrap().parsed
        self.code = code_result.code
        try:
            _code = json.loads(self.code)["code"] # Sometimes the code is wrapped in a json object
            self.code = _code
        except Exception as e:
            pass
        return result
    # @abstractmethod
    async def async_run(self) -> Result[Any, Exception]: 
        agent = create_code_block_generation_agent()
        result = await agent.async_run("", description=self.description, dependencies="\n".join([dep.full_str() for dep in self.dependencies]), dependents="\n".join([dep.full_str() for dep in self.dependents]))
        code_result = result.unwrap().parsed
        self.code = code_result.code
        try:
            _code = json.loads(self.code)["code"]
            self.code = _code
        except Exception as e:
            pass
        return result

