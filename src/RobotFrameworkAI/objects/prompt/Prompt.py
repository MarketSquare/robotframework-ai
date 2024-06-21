from dataclasses import dataclass
from typing import List, Dict
from RobotFrameworkAI.objects.prompt.PromptConfig import PromptConfig
from RobotFrameworkAI.objects.prompt.PromptMessage import PromptMessage
from RobotFrameworkAI.objects.prompt.PromptMetadata import PromptMetadata
from RobotFrameworkAI.objects.prompt.ai_tool_data.AIToolData import AIToolData

@dataclass
class Prompt:
    """
    The object that holds all information needed to generate a response from an AI model.

    Prompt object are used as a standardized way of communication between modules and AI models.
    Each module creates a Prompt and sends it to the AI_Interface. The AI_Interface will then send it to
    the appropriate AIModelStrategy, which in turn unpacks this object and sends the data to the AI model.

    Attributes:
        config (PromptConfig): Configuration for the prompt.
        message (List[PromptMessage]): List of messages to be sent to the AI model.
        parameters (Dict): Parameters controlling the AI model's response.
        metadata (PromptMetadata): Metadata for logging and tracking.
        ai_tool_data (AIToolData): Additional data for AI tools.
    """
    config: PromptConfig
    message: List[PromptMessage]
    parameters: Dict
    metadata: PromptMetadata
    ai_tool_data: AIToolData
