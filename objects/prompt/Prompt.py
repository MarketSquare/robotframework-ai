from objects.prompt.PromptConfig import PromptConfig
from objects.prompt.PromptMetadata import PromptMetadata


class Prompt:
    def __init__(self, config:PromptConfig, message, parameters:dict, metadata:PromptMetadata) -> None:
        self.config = config
        self.message = message
        self.parameters = parameters
        self.metadata = metadata