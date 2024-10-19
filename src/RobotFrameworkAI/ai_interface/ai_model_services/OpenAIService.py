import os
from openai import OpenAI
from typing import Optional

from RobotFrameworkAI.ai_interface.ai_model_services.AIModelStrategy import AIModelStrategy
from RobotFrameworkAI.objects.response.Response import Response
from RobotFrameworkAI.objects.response.ResponseMetadata import ResponseMetadata
import logging

from RobotFrameworkAI.ai_interface.ai_model_services.openai_tools.OpenAITool import OpenAITool

# List of allowed file extensions
ALLOWED_EXTENSIONS = {
    "c", "cpp", "css", "csv", "docx", "gif", "html", "java", "jpeg", "jpg", "js", "json", "md", "pdf", 
    "php", "png", "pptx", "py", "rb", "tar", "tex", "ts", "txt", "webp", "xlsx", "xml", "zip"
}

logger = logging.getLogger(__name__)


class OpenAIService(AIModelStrategy):
    """
    The class in charge of handling communication with the OpenAI API 
    
    This class is an implementation of the abstract class AIModelStrategy.
    Prompts directed at the OpenAI API will get sent to the right OpenAI AI tool.
    All the logic doing that can be found in the abstract class AIModelStrategy. 
    """

    def __init__(self, openai_key: Optional[str] = None) -> None:
        super().__init__()
        self.name = "openai"

        # Use the provided key or fallback to the environment variable
        self.openai_key = openai_key or os.getenv("OPENAI_KEY")
        if not self.openai_key:
            raise ValueError("OpenAI API key must be provided either as a parameter or via the OPENAI_KEY environment variable.")

        print("OpenAI API key:", self.openai_key)
        client = OpenAI(api_key=self.openai_key)
        self.ai_tools = self._discover_tools("openai_tools", OpenAITool, client)
