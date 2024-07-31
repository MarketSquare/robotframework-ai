from dataclasses import dataclass, field
import time
from typing import Optional

@dataclass
class ResponseMetadata:
    """
    An object containing the metadata for the Response.

    It contains data about:
    The AI model that created the Response.
    The model of the AI model.
    The reason why the AI model finished the Response.
    The amount of tokens used in the prompt.
    The amount of tokens used in the response.
    The time of completion. 
    """
    ai_tool: str
    ai_model: str
    model: str
    finish_reason: Optional[str] = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    time: int = field(default_factory=lambda: int(time.time()))
    kwargs: dict = field(default_factory=dict)
