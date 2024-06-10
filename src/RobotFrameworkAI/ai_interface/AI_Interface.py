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
    This class handles the communication between modules and the AI models.
    This class together with the classes in the ai_model_service folder form a strategy pattern.
    In this strategy pattern, this class serves the role as the context.
    The AI model strategies will be used it.

    After creating a new strtegy, it will dynamically be discovered, requiring no changes to this class.
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
                continue
            
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, AIModelStrategy) and obj is not AIModelStrategy:
                    try:
                        instance = obj()
                        ai_models[instance.name] = instance
                        logger.debug(f"Discovered AI model strategy: {instance.name} in class {name}")
                    except Exception as e:
                        logger.error(f"Failed to instantiate {name}: {e}")
        return ai_models

    def call_ai_tool(self, prompt):
        ai_model = prompt.config.ai_model
        try:
            if ai_model not in self.ai_models:
                raise ValueError(f"Invalid ai_model: `{ai_model}`. Valid ai_models are: `{'`, `'.join(self.ai_models)}`")
        except Exception as e:
            logger.error(e)
            raise

        ai_model_strategy = self.ai_models[ai_model]
        print(f"Request being handled by {ai_model}...")
        
        logger.debug(f"Sending prompt to {ai_model}: {prompt}")

        response = ai_model_strategy.call_ai_tool(prompt)

        logger.debug(f"Recieved response from {ai_model}: {response}")
        return response


        


