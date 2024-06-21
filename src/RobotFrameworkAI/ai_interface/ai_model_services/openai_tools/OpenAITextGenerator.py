from openai import OpenAI
from RobotFrameworkAI.ai_interface.ai_model_services.openai_tools.OpenAITool import OpenAITool
from RobotFrameworkAI.ai_interface.ai_model_tools.TextGeneratorTool import TextGeneratorTool
from RobotFrameworkAI.objects.response.Response import Response
from RobotFrameworkAI.objects.response.ResponseMetadata import ResponseMetadata
import logging


logger = logging.getLogger(__name__)


class OpenAITextGenerator(OpenAITool, TextGeneratorTool):
    """
    The AI tool in charge of handling all text generation for OpenAI

    Given a prompt, will send it to OpenAI API, and return a Response.
    """
    def __init__(self, client) -> None:
        OpenAITool.__init__(self)
        TextGeneratorTool.__init__(self)
        self.client:OpenAI = client
    
    def call_ai_tool(self, prompt):
        model = self.default_model if prompt.config.model is None else prompt.config.model
        messages = self.format_prompt_messages(prompt.message.system, prompt.message.user, prompt.message.history)
        arguments = prompt.parameters
        chat_completion = self.client.chat.completions.create(
            model = model,
            messages = messages,
            response_format= prompt.config.response_format,
            max_tokens = arguments["max_tokens"],
            temperature = arguments["temperature"],
            top_p = arguments["top_p"],
            frequency_penalty = arguments["frequency_penalty"],
            presence_penalty = arguments["presence_penalty"]
        )
        logger.debug(f"{self.ai_model_name} {self.tool_name}: {chat_completion}")
        metadata = ResponseMetadata(
            self.tool_name,
            self.ai_model_name,
            model,
            chat_completion.choices[0].finish_reason,
            chat_completion.usage.prompt_tokens,
            chat_completion.usage.completion_tokens,
            chat_completion.created
        )
        response = Response(
            chat_completion.choices[0].message.content,
            metadata
        )
        return response