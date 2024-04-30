

from ai_interface.ai_model_services.GeminiService import GeminiService
from ai_interface.ai_model_services.OpenAIService import OpenAIService



class AI_Interface:

    def __init__(self) -> None:
        self.ai_models = {
            "openai": OpenAIService(),
            "gemini": GeminiService(),
        }
    
    def send_prompt(self, module:str, ai_model:str, message:list, max_tokens:int, model:str, temperature:float, top_p:float, frequency_penalty:float, presence_penalty:float):
        if ai_model not in self.ai_models:    
            raise ValueError(f"Invalid ai_model: '{ai_model}'. Valid models are: {', '.join(self.ai_models)}")
        ai_model_strategy = self.ai_models[ai_model]
        print(f"Request being handled by {ai_model}...")
        response = ai_model_strategy.send_prompt(message, max_tokens, model, temperature, top_p, frequency_penalty, presence_penalty)
        return response

        

        


