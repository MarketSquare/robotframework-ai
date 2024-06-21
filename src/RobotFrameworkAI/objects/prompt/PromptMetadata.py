from dataclasses import dataclass, field
import time

@dataclass
class PromptMetadata:
    """
    An object containing the metadata for the Prompt.

    It contains data about what module created the Prompt and at what time it was created. 
    """
    module: str
    time: int = field(default_factory=lambda: int(time.time()))
    kwargs: dict = field(default_factory=dict)
