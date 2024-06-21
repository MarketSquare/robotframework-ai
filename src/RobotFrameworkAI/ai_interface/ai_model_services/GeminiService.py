


from RobotFrameworkAI.ai_interface.ai_model_services.AIModelStrategy import AIModelStrategy


class GeminiService(AIModelStrategy):    
    """
    THIS CLASS IS JUST AN EXAMPLE FOR NOW AND SHOULD/CAN NOT BE USED AS IT DOES NOTHING

    This class is an implementation of the AIModelStrategy interface.
    This is an strategy to handle task of responding to prompts.
    This strategy does so by using the API from Google.
    """
    def __init__(self) -> None:
        super().__init__()
        self.name = "gemini"
        client = None
        # self.ai_tools = self._discover_tools("gemini_tools", GeminiTool, client)
        
    def send_prompt(self, prompt):
        return "Beep boop"