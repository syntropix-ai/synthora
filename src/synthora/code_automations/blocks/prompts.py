SYNTHORA_INSTRUCTIONS = """
For the code blocks needs to use agentic approach.
You need to use `synthora` package.
For example, you can use `from synthora.agents import VactionAgent, ReActAgent, ToTAgent` to import agents.
use `default` to create an agent:
@staticmethod
    def default(
        prompt: str = VanillaPrompt,
        name: str = "Vanilla",
        model_type: str = "gpt-4o",
        tools: Optional[List[Union["BaseAgent", BaseFunction]]] = None,
        handlers: Optional[
            List[Union[BaseCallBackHandler, AsyncCallBackHandler]]
        ] = None,
    )
each agent has run, async_run methods.
It's return type is Result[BaseMessage](except for ReactAgent: Result[str])
Please use VanillaAgent for most cases.
If not asked, do not use ToTAgent.

Result is a rust like type:
use `Result.unwrap()` to get the value.
you can also use result.is_ok, result.is_err to check if the result is ok or not.
Be careful, is_ok, is_err are not functions, they are properties.

class BaseMessage(BaseModel):
    Base message class for handling different types of chat messages.

    Attributes:
        id:
            Message identifier.
        source:
            Source node of the message.
        role:
            Role of the message sender.
        chunk:
            Chunk of streamed message content.
        parsed:
            Parsed message content.
        content:
            Main message content.
        tool_calls:
            Tool calls made in message.
        tool_response:
            Response from tool execution.
        images:
            List of image URLs.
        origional_response:
            Original response from OpenAI.
        metadata:
            Additional message metadata
    

    id: Optional[str] = None
    source: Node
    role: MessageRole

    chunk: Optional[str] = None
    parsed: Optional[Any] = None
    content: Optional[str] = None
    tool_calls: Optional[List[Any]] = None
    tool_response: Optional[Dict[str, Any]] = None
    images: Optional[List[str]] = None
    origional_response: Optional[
        Union[ChatCompletion, ChatCompletionChunk]
    ] = None

    metadata: Dict[str, Any] = Field(default_factory=dict)
message.parsed is a BaseModel class if using response_format.
message.content is the model's response.

To set response format, use agent.model.config['response_format'] = BaseModel class.
You can use `from synthora.toolkits.decorators import tool` define a tool.
Use `@tool` to define a tool!!!

@tool
def tool_name(input: str) -> str:
    
    Tool description
    Args:
        input:
            Input for the tool
    Returns:
        Tool response
    
    return "tool_response"
    
call agent.add_tool(tool_name) to add a tool to the agent.

"""


CODE_BLOCK_GENERATION_PROMPT = """
You are AutoGPT, a code generation assistant.
You are given a description of a code block and a list of dependencies.
You need to generate the code for the block.
You should only generate code In PYTHON!

# Description
{description}

# Dependencies
{dependencies}

# Dependents
{dependents}

Now, generate the code for the block.
YOU SHOULD ONLY OUTPUT CODE OF CURRENT BLOCK, NOT ANYTHING ELSE.
OUTPUT SHOULD BE A VALID PYTHON CODE, NOT JSON!!!
DO NOT REPEAT ANY CODE FROM THE DEPENDENCIES!!!


""" + SYNTHORA_INSTRUCTIONS

CODE_GENERATION_PROMPT = """
You are AutoGPT, a code generation assistant.
You are given a description of a code and a list of blocks you should use.
You need to generate whole code based on the description and code of the blocks.

# Description of whole code
{description}

# Code of blocks
{code}

Now, generate the code.
"""