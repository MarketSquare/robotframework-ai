

from ai_interface.ai_model_services.GeminiService import GeminiService
from ai_interface.ai_model_services.OpenAIService import OpenAIService



class AI_Interface:

    def __init__(self) -> None:
        self.ai_models = {
            "openai": OpenAIService(),
            "gemini": GeminiService(),
        }
    
    def send_prompt(self, prompt):
        ai_model = prompt.config.ai_model
        if ai_model not in self.ai_models:    
            raise ValueError(f"Invalid ai_model: '{ai_model}'. Valid models are: {', '.join(self.ai_models)}")
        ai_model_strategy = self.ai_models[ai_model]
        print(f"Request being handled by {ai_model}...")
        response = ai_model_strategy.send_prompt(prompt)
        return response

        

        


