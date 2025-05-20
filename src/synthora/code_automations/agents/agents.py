from typing import List
from synthora.agents.vanilla_agent import VanillaAgent

from synthora.callbacks.rich_output_handler import RichOutputHandler
from synthora.code_automations.agents.prompts import BLOCK_GENERATION_PROMPT, CODE_BLOCK_GENERATION_PROMPT, CODE_GENERATION_PROMPT
from pydantic import BaseModel, Field

from synthora.toolkits.decorators import tool

@tool
def provide_code(code: str) -> str:
    """
    Provide the code for the block.
    Args:
        code:
            The code for the block. must have import, block definition and block logic, and print the result.
    Returns:
        The result of the code.
    """
    return "Done, ask user check the code and provide comments."

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

def create_code_block_generation_chat_agent(model: str = "gpt-4o") -> VanillaAgent:
    agent = VanillaAgent.default(
        model_type=model,
        prompt=BLOCK_GENERATION_PROMPT,
        tools=[provide_code],
        handlers=[RichOutputHandler()]
    )
    agent.model.set_stream(True)
    return agent