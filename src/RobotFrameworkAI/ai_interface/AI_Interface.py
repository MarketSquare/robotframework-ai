

from RobotFrameworkAI.ai_interface.ai_model_services.GeminiService import GeminiService
from RobotFrameworkAI.ai_interface.ai_model_services.OpenAIService import OpenAIService



class AI_Interface:
    """
    This class handles the communication between modules and the AI models.
    This class together with the classes in the ai_model_service folder form a strategy pattern.
    In this strategy pattern, this class serves the role as the context.
    The AI model strategies will be used it.

    After creating a new strtegy, adding it to the ai_models attribute allows it to be used.
    """

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

        

        


