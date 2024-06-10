import time


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
    def __init__(self, ai_tool:str, ai_model: str, model: str, finish_reason: str = None, prompt_tokens: int = 0, completion_tokens: int = 0, time: int = int(time.time()), **kwargs) -> None:
        self.ai_tool = ai_tool
        self.ai_model = ai_model
        self.model = model
        self.finish_reason = finish_reason
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.time = time
        self.kwargs = kwargs


    def __str__(self):
        additional_args = ', '.join([f"({key}: {value})" for key, value in self.kwargs.items()])
        return f"(AI Tool: {self.ai_tool}), (AI Model: {self.ai_model}), (Model: {self.model}), (Finish Reason: {self.finish_reason}), (Prompt Tokens: {self.prompt_tokens}), (Completion Tokens: {self.completion_tokens}), (Time: {self.time})" + (f", {additional_args}" if additional_args else "")