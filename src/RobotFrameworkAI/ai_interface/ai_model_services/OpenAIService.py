import os
from openai import OpenAI

from RobotFrameworkAI.ai_interface.ai_model_services.AIModelStrategy import AIModelStrategy
from RobotFrameworkAI.objects.response.Response import Response
from RobotFrameworkAI.objects.response.ResponseMetadata import ResponseMetadata


class OpenAIService(AIModelStrategy):
    """
    This class is an implementation of the AIModelStrategy interface.
    This is an strategy to handle task of responding to prompts.
    This strategy does so by using the API from OpenAI.
    """
    def __init__(self) -> None:
        super().__init__()
        self.name = "openai"
        key = os.environ["OPENAI_KEY"]
        self.ai_model = OpenAI(api_key=key)
        self.default_model = "gpt-3.5-turbo"

    def send_prompt(self, prompt):
        model = prompt.config.model
        if prompt.config.model is None:
            model = self.default_model
        self.validate_prompt(model)
        arguments = prompt.parameters
        chat_completion = self.ai_model.chat.completions.create(
            model = model,
            messages = prompt.message,
            response_format= prompt.config.response_format,
            max_tokens = arguments["max_tokens"],
            temperature = arguments["temperature"],
            top_p = arguments["top_p"],
            frequency_penalty = arguments["frequency_penalty"],
            presence_penalty = arguments["presence_penalty"]
        )
        metadata = ResponseMetadata(
            self.name,
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
    
    def validate_prompt(self, model:str):
        models = ["gpt-3.5-turbo"]
        if model not in models:
            raise ValueError(f"Invalid value '{model}' for 'model'. Model not found in the available models.")
