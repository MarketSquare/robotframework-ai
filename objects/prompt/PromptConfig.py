class PromptConfig:
    def __init__(self, ai_model:str, model:str, response_format:dict, **kwargs) -> None:
        self.ai_model = ai_model
        self.model = model
        self.response_format = response_format
        self.kwargs = kwargs
