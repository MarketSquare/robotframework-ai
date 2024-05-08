class ResponseMetadata:
    def __init__(self, ai_model: str, finish_reason: str, prompt_tokens: int, completion_tokens: int, time: int, **kwargs) -> None:
        self.ai_model = ai_model
        self.finish_reason = finish_reason
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.time = time
        self.kwargs = kwargs
