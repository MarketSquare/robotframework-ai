from dataclasses import dataclass, field
from typing import List, Optional
from RobotFrameworkAI.objects.prompt.ai_tool_data.AIToolData import AIToolData

@dataclass
class AssistantData(AIToolData):
    """
    Additional data used when using an AI assistant tool.

    Attributes:
        action (str): Determines what you want to do with the AI assistant.
        id (Optional[str]): Identifier for the assistant data.
        name (Optional[str]): Name for the assistant data.
        instructions (str): Instructions for the assistant.
        file_paths (Optional[List[str]]): List of paths to files/folders to attach to the assistant.
    """
    action: str
    id: Optional[str] = None
    name: Optional[str] = None
    instructions: str = ""
    file_paths: Optional[List[str]] = None

    def __post_init__(self):
        if self.file_paths is None:
            self.file_paths = []
