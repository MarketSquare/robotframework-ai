from dataclasses import dataclass, field
from typing import List

@dataclass
class PromptMessage:
    """
    This object contains the messages for the prompt.

    It includes a system message, a user message, and optionally a history of previous messages.
    The history is a list of dictionaries, where each dictionary represents a past message interaction.
    """
    system: str
    user: str
    history: List[dict] = field(default_factory=list)
