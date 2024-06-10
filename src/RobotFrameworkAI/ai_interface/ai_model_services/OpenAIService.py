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
    This class is an implementation of the AIModelStrategy interface.
    This is an strategy to handle task of responding to prompts.
    This strategy does so by using the API from OpenAI.
    """
    def __init__(self) -> None:
        super().__init__()
        self.name = "openai"
        client = OpenAI(api_key=os.environ["OPENAI_KEY"])
        self.ai_tools = self._discover_tools("openai_tools", OpenAITool, client)


    # def

    # def assist():
    #     pass

    # def create_assistant(self):
    #     assistant = self.ai_model.beta.assistants.create(
    #         name="Test error explainer",
    #         instructions="""When a Robot Framework test fails, you get called and read there code.
    #         Based on the code you explain why the test fails or give an error.
    #         You then also give suggestion on how to improve said code so the test succeeds""",
    #         model="gpt-3.5-turbo",
    #         tools=[{"type": "file_search"}],
    #     )
    #     return assistant

    # def collect_files():
    #     pass

    # def add_files(self):
    #     self.ai_model.beta.vector_stores.create(name="Code")
