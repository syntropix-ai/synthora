from typing import List
from synthora.agents.vanilla_agent import VanillaAgent

from synthora.code_automations.blocks.prompts import CODE_BLOCK_GENERATION_PROMPT, CODE_GENERATION_PROMPT
from pydantic import BaseModel, Field

class CodeResult(BaseModel):
    code: str = Field(description="Python code for the block")

def create_code_block_generation_agent(model: str = "gpt-4o") -> VanillaAgent:
    agent = VanillaAgent.default(
        model_type=model,
        prompt=CODE_BLOCK_GENERATION_PROMPT
    )
    agent.model.config['response_format'] = CodeResult
    return agent

def create_code_generation_agent(model: str = "gpt-4o") -> VanillaAgent:
    agent = VanillaAgent.default(
        model_type=model,
        prompt=CODE_GENERATION_PROMPT
    )
    agent.model.config['response_format'] = CodeResult
    return agent