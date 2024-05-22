import time


class PromptMetadata:
    """
    An object containing the metadata for the Prompt.

    It contains data about what module created the Prompt and at what time it was created. 
    """
    def __init__(self, module: str, **kwargs) -> None:
        self.module = module
        self.time = int(time.time())    # Current time in unix
        self.kwargs = kwargs
