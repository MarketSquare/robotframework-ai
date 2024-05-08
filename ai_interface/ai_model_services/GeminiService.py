


from ai_interface.ai_model_services import AIModelStrategy


class GeminiService():
    def __init__(self) -> None:
        self.ai_model = None
        
    def send_prompt(self, prompt):
        return "Beep boop"