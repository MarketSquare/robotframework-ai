class PromptConfig:
    """
    This object contains the configuration data for the Prommpt.

    It contains the information about what AI model and model to use and how to format the response.
    """
    def __init__(self, ai_model:str, model:str, response_format:dict, **kwargs) -> None:
        self.ai_model = ai_model
        self.model = model
        self.response_format = response_format
        self.kwargs = kwargs
