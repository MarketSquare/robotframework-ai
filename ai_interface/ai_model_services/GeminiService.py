


class GeminiService:
    def __init__(self) -> None:
        self.ai_model = None
        
    def send_prompt(self, message:list, max_tokens:int, model:str, temperature:float, top_p:float, frequency_penalty:float, presence_penalty:float):
        return "Beep boop"