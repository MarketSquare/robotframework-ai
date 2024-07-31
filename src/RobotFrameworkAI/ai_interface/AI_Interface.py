import importlib
import inspect
import os
import pkgutil
import sys
from RobotFrameworkAI.ai_interface.ai_model_services.GeminiService import GeminiService
from RobotFrameworkAI.ai_interface.ai_model_services.OpenAIService import OpenAIService
import logging

from RobotFrameworkAI.ai_interface.ai_model_services.AIModelStrategy import AIModelStrategy


logger = logging.getLogger(__name__)





class AI_Interface:
    """
    This class and all the classes below it, handle communicating with AI models.
    To put it simply, this class accepts a Prompt object and outputs a Response object.

    The structure of the AI interface and all classes under it, works by having 1 central class accepting all Prompts.
    That is this class. Under this central class there is a class for each specific AI model. These classes are in charge
    of handling all Prompts directed at that specific AI model.
    
    Under these classes, it splits once more. AI models have different types of tools like text_generator and assistant.
    For each of these types of tools there is a class responsible for that. These classes are at bottom of this hierarchy.
    These classes eventually communicate with the AI models and are in charge of creating the Response.

    All the steps before that effectively "route" to the right AI tool class. This is similar to
    how you might travel to other countries. First you take a plane to that country, then you take the train to the right city,
    then you take the bus to closest to your destination and then you walk the rest.

    All classes specific for AI models inherit from a common class, the AIModelStrategy. This class contains attributes and methods
    used by all AI model specific classes. Similarly, all tools specific for an AI model, also inherit from a common class. Once again
    all tools specific for that share common attributes and methods.

    Because specific AI tool types aren't limited to specific AI models, there is another similar hierarchy structure.
    In the above case, the classes are first divided by AI model and then by AI tool type. Here we capture data common among AI tools
    from the same AI model. It is also possible to capture data common among AI tools from the same type of AI tools. So instead of
    grouping AI tools by their AI model, they can be grouped based on the type of AI tool.

    By grouping AI tools on their type of tool aswell, it allows for common attributes and methods specific for a type of tool
    to be shared. This ultimate makes it so the classes at the bottom of hierarchy inherit from both an AI model specific class
    aswell as an AI tool type specific class.

    Another way to look at it is like a table. On the top row there are different AI models, with different types of AI tool types
    on the left most column. Each specific AI tool will belong in a column and row. Each AI tool will both inherit from the AI model
    in the column the AI tool is and in the AI tool type in the row of the AI tool.
    """

    def __init__(self) -> None:
        self.ai_models: list[AIModelStrategy] = self._discover_ai_models()

    def _discover_ai_models(self):
        """
        Dynamically collects all AIModelStrategy implementations in the ai_model_service folder.

        A dictionary will be created with the name of each AIModelStrategy as the key and an instance as value.
        The name comes from the name attribute in the implementation of the AIModelStrategy.
        """
        ai_models = {}
        package = 'RobotFrameworkAI.ai_interface.ai_model_services'
        package_path = os.path.join(os.path.dirname(__file__), 'ai_model_services')
        
        logger.debug(f"Looking for modules in package path: {package_path}")

        if not os.path.exists(package_path):
            logger.error(f"Package path does not exist: {package_path}")
            return ai_models

        for _, module_name, _ in pkgutil.iter_modules([package_path]):
            logger.debug(f"Found module: {module_name}")
            try:
                module = importlib.import_module(f"{package}.{module_name}")
                logger.debug(f"Imported module: {module_name}")
            except Exception as e:
                logger.error(f"Failed to import module {module_name}: {e}")
                raise
            
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, AIModelStrategy) and obj is not AIModelStrategy:
                    try:
                        instance = obj()
                        ai_models[instance.name] = instance
                        logger.debug(f"Discovered AI model strategy: {instance.name} in class {name}")
                    except Exception as e:
                        logger.error(f"Failed to instantiate {name}: {e}")
                        raise
        return ai_models

    def call_ai_tool(self, prompt):
        """
        Sends the prompt to the right AI model service class

        Depending on the AI model assigned to the Prompt sends the Prompt to the right AI model strategy class.
        Will raise an error if the AI model doesn't exists.

        Those classes also have a call_ai_tool method which further sends the Prompt to the specific AI tool type.
        """
        ai_model = prompt.config.ai_model
        if ai_model not in self.ai_models:
            error_message = f"Invalid ai_model: `{ai_model}`. Valid ai_models are: `{'`, `'.join(self.ai_models)}`"
            logger.error(error_message)
            raise ValueError(error_message)

        ai_model_strategy = self.ai_models[ai_model]
        print(f"Request being handled by {ai_model}...")
        
        logger.debug(f"Sending prompt to {ai_model}: {prompt}")

        response = ai_model_strategy.call_ai_tool(prompt)

        logger.debug(f"Recieved response from {ai_model}: {response}")
        return response


        


