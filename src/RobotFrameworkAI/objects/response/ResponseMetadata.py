class ResponseMetadata:
    """
    An object containing the metadata for the Response.

    It contains data about:
    The AI model that created the Response.
    The model of the AI model.
    The reason why the AI model finished the Response.
    The amount of tokens used in the prompt.
    The amount of tokens used in the response.
    The time of completion. 
    """
    def __init__(self, ai_model: str, model: str, finish_reason: str, prompt_tokens: int, completion_tokens: int, time: int, **kwargs) -> None:
        self.ai_model = ai_model
        self.model = model
        self.finish_reason = finish_reason
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.time = time
        self.kwargs = kwargs
