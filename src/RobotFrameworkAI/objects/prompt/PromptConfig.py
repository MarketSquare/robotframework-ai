from dataclasses import dataclass
from typing import Dict

@dataclass
class PromptConfig:
    """
    This object contains the configuration data for the Prompt.

    It contains the information about what AI tool and model to use and how to format the response.
    """
    ai_tool: str
    ai_model: str
    model: str
    response_format: Dict
    kwargs: Dict = None
