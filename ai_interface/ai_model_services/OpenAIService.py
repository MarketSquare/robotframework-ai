from dotenv import load_dotenv
from openai import OpenAI


class OpenAIService:
    def __init__(self) -> None:
        load_dotenv()
        self.ai_model = OpenAI()

    def send_prompt(self, message:list, max_tokens:int, model:str, temperature:float, top_p:float, frequency_penalty:float, presence_penalty:float):
        self.validate_prompt(model)
        return self.ai_model.chat.completions.create(
            model = model,
            messages = message,
            response_format={ "type": "json_object" },
            max_tokens = max_tokens,
            temperature = temperature,
            top_p = top_p,
            frequency_penalty = frequency_penalty,
            presence_penalty = presence_penalty,
        )
    
    def validate_prompt(self, model:str):
        models = ["gpt-3.5-turbo"]
        if model not in models:
            raise ValueError(f"Invalid value '{model}' for 'model'. Model not found in the available models.")
