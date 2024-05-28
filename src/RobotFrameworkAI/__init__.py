from robot.api.deco import keyword, library
from functools import wraps
import inspect

from .modules.real_test_data_generator.RealTestDataGenerator import RealTestDataGenerator
from .modules.chatbot.Chatbot import Chatbot
from .logger.logger_config import setup_logging

@library
class RobotFrameworkAI(RealTestDataGenerator, Chatbot):
    """
    """
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
