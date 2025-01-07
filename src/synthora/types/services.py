from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class HttpAgentRequest(BaseModel): # type: ignore[no-redef]
    message: str
    args: Optional[List[Any]] = None
    kwargs: Optional[Dict[str, Any]] = None
