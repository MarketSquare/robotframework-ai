import time


class PromptMetadata:
    def __init__(self, module: str, **kwargs) -> None:
        self.module = module
        self.time = int(time.time())    # Current time in unix
        self.kwargs = kwargs
