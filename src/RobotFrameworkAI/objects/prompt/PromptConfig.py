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

    def __str__(self):
        additional_args = ', '.join([f"({key}: {value})" for key, value in self.kwargs.items()])
        return f"(AI Model: {self.ai_model}), (Model: {self.model}), (Response Format: {self.response_format})" + (f", {additional_args}" if additional_args else "")
