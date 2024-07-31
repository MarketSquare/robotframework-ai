from pathlib import Path
from typing import List
from robot.api.deco import keyword, library
from functools import wraps
from robotlibcore import DynamicCore
import inspect

from .modules.real_test_data_generator.RealTestDataGenerator import RealTestDataGenerator
from .modules.chatbot.Chatbot import Chatbot
from .modules.assistant.Assistant import Assistant
from .logger.logger import setup_logging

@library
class RobotFrameworkAI(DynamicCore):
    """
    RobotFrameworkAI is a custom library for Robot Framework that integrates AI functionalities,
    including generating real test data, interacting with a chatbot, and managing AI assistants.
    """
    def __init__(self) -> None:
        """
        Initializes the RobotFrameworkAI library with necessary components like RealTestDataGenerator,
        Chatbot, and Assistant, which are integrated to provide AI capabilities to Robot Framework.
        """
        libraries = [RealTestDataGenerator(), Chatbot(), Assistant()]
        DynamicCore.__init__(self, libraries)

    @keyword
    @wraps(setup_logging)
    def setup_logging(self, *args, **kwargs):
        # Dynamically fetch the signature of the original setup_logging function
        sig = inspect.signature(setup_logging)
        
        # Bind the provided arguments to the original function's signature
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        # Call the original setup_logging function with the bound arguments
        setup_logging(*bound_args.args, **bound_args.kwargs)

ROBOT_LIBRARY_SCOPE = "GLOBAL"
