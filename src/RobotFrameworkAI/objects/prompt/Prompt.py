from RobotFrameworkAI.objects.prompt.PromptConfig import PromptConfig
from RobotFrameworkAI.objects.prompt import PromptMetadata
from RobotFrameworkAI.objects.prompt.ai_tool_data.AIToolData import AIToolData


class Prompt:
    """
    The object that holds all information needed to generate a response from an AI model.

    Prompt object are used as a standardized way of communication between modules and AI models.
    Each module creates a Prompt and sends it to the AI_Interface. The AI_Interface will then send it to
    the appropriate AIModelStrategy, which in turn unpacks this object and sends the data to the AI model.

    It has a config, which contains the information about what AI model and model to use and how to format the response.
    The message is a list containing dictionaries which contain the messages that will be sent to the AI model.
    Parameters is a dictionary with parameters that control how the AI model generates data.
    The metadata is an object that contains information about the Prompt itself, this can be used for logging.
    """
    def __init__(self, config:PromptConfig, message:list, parameters:dict, metadata:PromptMetadata, ai_tool_data: AIToolData) -> None:
        self.config = config
        self.message = message
        self.parameters = parameters
        self.metadata = metadata
        self.ai_tool_data = ai_tool_data

    def __str__(self):
        parameters_str = ', '.join([f"({key}: {value})" for key, value in self.parameters.items()])
        return f"Prompt: {self.config}, (Message: {self.message}), {parameters_str}, {self.metadata}, {self.ai_tool_data}"
