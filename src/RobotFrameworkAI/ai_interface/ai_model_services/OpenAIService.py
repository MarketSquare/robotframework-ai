import os
from openai import OpenAI

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
    Prompts directed at the OpenAI API, will get send to the right OpenAI AI tool.
    All the logic doing that can be found in the abstract class AIModelStrategy. 
    """
    def __init__(self) -> None:
        super().__init__()
        self.name = "openai"
        client = OpenAI(api_key=os.environ["OPENAI_KEY"])
        self.ai_tools = self._discover_tools("openai_tools", OpenAITool, client)
