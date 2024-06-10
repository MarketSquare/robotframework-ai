import importlib
import inspect
import logging
import os
import pkgutil


logger = logging.getLogger(__name__)

class AIModelStrategy:
    """
    The interface class for AI model strategies.
    A prompt can be handled by different AI models.
    Each AI model can be used as a strategy to perform the task of responding to the prompt.

    To add a new AI model, create a new class in this folder and have it inherit this interface.
    Create the logic for unpacking a Prompt object, sending it to the AI model and pack its 
    response in a Response object.

    Make sure the send_prompt method is implemented to accept the Prompt and return the Response.
    Adding an object of this class to the ai_models in the AI_Interface class will allow you to
    to use that AI model for the generation of data.
    """
    def __init__(self) -> None:
        self.ai_tools = None
        self.name = None

    def _discover_tools(self, package: str, tool_interface, ai_client):
        """
        Dynamically collects all tool implementations in the specified package.

        A dictionary will be created with the tool attribute as the key and an instance as value.
        """
        tools = {}

        package_path = os.path.join(os.path.dirname(__file__), package)
        package = "RobotFrameworkAI.ai_interface.ai_model_services." + package

        logger.debug(f"Looking for tools in package path: {package_path}")

        if not os.path.exists(package_path):
            logger.error(f"Package path does not exist: {package_path}")
            return tools

        for _, module_name, _ in pkgutil.iter_modules([package_path]):
            logger.debug(f"Found module: {module_name}")
            try:
                module = importlib.import_module(f"{package}.{module_name}")
                logger.debug(f"Imported module: {module_name}")
            except Exception as e:
                logger.error(f"Failed to import module {module_name}: {e}")
                continue

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, tool_interface) and obj is not tool_interface:
                    try:
                        instance = obj(ai_client)
                        tools[instance.tool_name] = instance
                        logger.debug(f"Discovered tool: {instance.tool_name} in class {name}")
                    except Exception as e:
                        logger.error(f"Failed to instantiate {name}: {e}")
                        raise
        return tools

    def call_ai_tool(self, prompt):
        model = prompt.config.model
        tool_name = prompt.config.ai_tool
        self.validate_tool(tool_name)
        tool = self.ai_tools[tool_name]
        self.validate_model(model, tool)

        return tool.call_ai_tool(prompt)

    def validate_tool(self, tool_name: str):
        """
        Validates whether the tool of the AI model is valid.

        A list of all valid models can be found in the respective tool folder of the AI model.
        For OpenAI that would be the openai_tools folder. Each class in that folder that inherits
        the OpenAITool class is a valid tool.

        The tool_name of that tool is the 2nd part of the class name in snakecase, in the case of
        OpenAITextGenerator, that would be text_generator. This tool_name is set in the tool class it
        inherits from. In this example that would be the TextGeneratorTool class.
        """
        if tool_name not in self.ai_tools:
            error_message = f"Invalid tool: `{tool_name}`. Valid tools are: `{', '.join(self.ai_tools.keys())}`"
            logger.error(error_message)
            raise ValueError(error_message)
        return True

    def validate_model(self, model:str, tool):
        """
        Validates whether the model of the AI model is valid.

        A list of all valid models can be found in the respective tool class of the AI model.
        For OpenAI that would be OpenAITool class. None is also valid as it will take the default model.
        """
        models = tool.models
        # Note that None is valid
        if model not in models and model is not None:
            error_message = f"Invalid model: `{model}`. Valid models are: `{'`, `'.join(models)}`"
            logger.error(error_message)
            raise ValueError(error_message)
        return True
