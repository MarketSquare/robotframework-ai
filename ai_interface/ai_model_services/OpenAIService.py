from dotenv import load_dotenv
import os
from openai import OpenAI

from ai_interface.ai_model_services import AIModelStrategy
from objects.response.Response import Response
from objects.response.ResponseMetadata import ResponseMetadata


class OpenAIService():
    def __init__(self) -> None:
        self.name = "openai"
        load_dotenv()
        self.ai_model = OpenAI(
            api_key=os.getenv("OPENAI_KEY")
        )
        self.default_model = "gpt-3.5-turbo"

    def send_prompt(self, prompt):
        model = prompt.config.model
        if prompt.config.model is None:
            model = self.default_model
        self.validate_prompt(model)
        parameters = prompt.parameters
        chat_completion = self.ai_model.chat.completions.create(
            model = model,
            messages = prompt.message,
            response_format= prompt.config.response_format,
            max_tokens = parameters["max_tokens"],
            temperature = parameters["temperature"],
            top_p = parameters["top_p"],
            frequency_penalty = parameters["frequency_penalty"],
            presence_penalty = parameters["presence_penalty"]
        )
        metadata = ResponseMetadata(
            self.name,
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
