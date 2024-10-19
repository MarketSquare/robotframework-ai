import importlib
import inspect
import os
import pkgutil
from robot.api.deco import keyword, library

from RobotFrameworkAI.modules.Module import Module
import logging

from RobotFrameworkAI.modules.real_test_data_generator.test_data_generators.TestDataGenerator import TestDataGenerator


logger = logging.getLogger(__name__)


@library
class RealTestDataGenerator(Module):
    """
    The RealTestDataGenerator is a module that generates real test data.

    The test data is real in the sense that it can or could (depending on the type of test data)
    exist in the real world. In the case of addresses, the generated addresses should exists, and
    thus should be findable on for example Google maps.

    The aim om this module is to overcome the issues the library Faker has.
    So if Faker can already generate generating email addresses with no issues, then the
    RealTestDataGenerator wont implement this logic.
    """
    def __init__(self) -> None:
        super().__init__()
        self.module_name = "real_test_data_generator"
        self.generators = self._discover_test_data_generators()
        self.ai_tool = "text_generator"
        # Set arguments
        self.type = None
        self.amount = 3
        self.format = None
        self.kwargs = {}

    def _discover_test_data_generators(self):
        """
        Dynamically collects all TestDataGenerator implementations in the test_data_generators folder.

        A dictionary will be created with the type of each TestDataGenerator as the key and an instance as value.
        The type comes from the type attribute in the implementation of the TestDataGenerator.
        """
        test_data_generators = {}
        package = 'RobotFrameworkAI.modules.real_test_data_generator.test_data_generators'
        package_path = os.path.join(os.path.dirname(__file__), 'test_data_generators')
        
        logger.debug(f"Looking for modules in package path: {package_path}")

        if not os.path.exists(package_path):
            logger.error(f"Package path does not exist: {package_path}")
            return test_data_generators

        for _, module_name, _ in pkgutil.iter_modules([package_path]):
            logger.debug(f"Found module: {module_name}")
            try:
                module = importlib.import_module(f"{package}.{module_name}")
                logger.debug(f"Imported module: {module_name}")
            except Exception as e:
                logger.error(f"Failed to import module {module_name}: {e}")
                raise
            
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, TestDataGenerator) and obj is not TestDataGenerator:
                    try:
                        instance = obj()
                        test_data_generators[instance.type] = instance
                        logger.debug(f"Discovered test data generator of type: {instance.type} in class {name}")
                    except Exception as e:
                        logger.error(f"Failed to instantiate {name}: {e}")
                        raise
        return test_data_generators

    @keyword
    def generate_test_data(
            self,
            ai_model:str=None,
            type:str=None,
            model:str=None,
            amount:int=None,
            format:str=None,
            max_tokens:int=None,
            temperature:float=None,
            top_p:float=None,
            frequency_penalty:float=None,
            presence_penalty:float=None,
            response_format:dict=None,
            **kwargs
        ):
        """
        RealTestDataGenerator
        =====================

        RealTestDataGenerator can generate test data for the Robot Framework similar to
        the library Faker. The RealTestDataGenerator however generates real existing data, using AI.

        To generate test data simply import the package and use the keyword: Generate Test Data
        This keyword takes various arguments, some being specific for the generation of certain
        types of test data.

        The following arguments can be used (arguments in bold are required):
        - *ai_model:str: The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
        - *type:str: The type of test data to create, e.g. "address", "user_data", etc. Currently supporting: "address"
        - amount:int: The amount of rows of test data to generate. Default = 3
        - format:str: The format in which the test data will be given. If None, will return a 2 dimensional list. Default = None
        - max_tokens:int: The token limit for a conversation. Both prompt and response tokens will count towards this limit. Default = 256
        - model:str: AI model specfic. The model of the AI model to be used. E.g. "gpt-3.5-turbo" when using the "openai" AI model.
            Default per AI model:
                - "openai" = "gpt-3.5-turbo"
        - temperature:float: This value determines the creativity of the AI model. Can be anything from 0-2. Default = 1
        - top_p:float: Similar to temperature. Determines the selection of tokens before selecting one.
            The higher the value the more less common tokens get added to the selection. Can be anything from 0-2. Default = 1
        - frequency_penalty:float: Penalizes more frequent token reducing the chance of it reappearing.
            Negative values encourage it to reuse tokens. Can be anything from -2 to 2. Default = 0
        - presence_penalty:float: Exact same as frequency_penalty except its scope is reduced to the immediate context.
            Can be anything from -2 to 2. Default = 0
        - kwargs:dict: Additional arguments can be supplied for specific types of test data. These will be explained in per type below

        Required arguments can also be set using setters.

        Addresses
        ---------

        When generating addresses additional argument are available. These arguments are as follows:
        - Country:str: The country from which to create addresses. If None, will generate an address from anywhere. Default = None


        AI models
        =========

        Each module in the RobotFramework-AI library can support multiple different AI models. Each AI model needs an API key for the generation of test data.
        This key gets read directly from your environment variables. Each AI model has their own API key. To define a key, create a new variable with the name of
        the AI model capitalized followed by "_KEY". Then set this variable to your key. 

        # Example API keys
        OPENAI_KEY=278bxw4m89monwxmu89wm98ufx8hwxfhqwifmxou09qwxp09jmx
        GEMINI_KEY=cavhjbcZCJKnvmzxcnzkcjkczckzcskjnjn7h38nwd923hdnind
        

        Setters
        =======

        Instead of providing all arguments through this keyword, it is also possible to set each argument beforehand. This way, when making repeated calls, arguments
        do not have to be supplied each time. After setting these arguments they will remain untill set again. When arguments are set and the keyword also has arguments
        supplied, then the supplied arguments will take priority.

        NOTE: Setting arguments will impact other modules aswell. This means that when setting the temperature to 2 that both the RealTestDataGenerator and the Chatbot
        will use this temperature from then on. This is only the case when both modules share arguments, the arguments that are shared are as followed: ai_model,
        model, max_tokens, temperature, top_p, frequency_penalty, presence_penalty, response_format.

        Each argument has its own setter, the name of the keyword is 'set' plus the name of the argument e.g. Set AI Model for AI Model.
        """     
        # If arguments are not given directly, get its default value. This is the value of the class attribute with the same name
        ai_model, model, max_tokens, temperature, top_p, frequency_penalty, presence_penalty, type, amount, format, kwargs = self.get_default_values_for_arguments(
            ai_model=ai_model,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature, 
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            type=type,
            amount=amount,
            format=format,
            kwargs=kwargs
        )
        # Response format should always be a json object
        response_format = { "type": "json_object" }
        # Log the arguments
        args = locals()
        args.pop("self")
        logger.debug(f"Calling keyword `Generate Test Data` with arguments: {', '.join(f'({k}: {v})' for k, v in args.items())}")
        # Validate arguments
        self.validate_input_arguments(
            type=type,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        generator = self.generators[type]
        system_message, user_message = generator.create_prompt_messages(amount, format, kwargs)
        prompt = self.create_prompt(
            self.ai_tool,
            ai_model,
            system_message,
            user_message,
            None,
            model,
            max_tokens,
            temperature,
            top_p,
            frequency_penalty,
            presence_penalty,
            response_format
        )
        logger.debug(f"Prompt: {prompt}")
        try:
            response = self.ai_interface.call_ai_tool(prompt)
            logger.debug(f"Response from AI tool: {response}")
            response = generator.format_response(response)
            logger.debug(f"Formatted response: {response}")
        except Exception as e:
            error_message = f"Failed to generate test data: {e}"
            logger.error(error_message)
            raise ValueError(error_message)

        logger.debug(f"Generated test data: {response}")
        return response

    # Validation methods
    def is_valid_type(self, type: str):
        if type not in self.generators:
            error_message = f"Invalid type: `{type}`. Valid type's are: `{'`, `'.join(self.generators)}`"
            logger.error(error_message)
            raise ValueError(error_message)
    
    # Setters
    @keyword
    def set_type(self, type: str = None):
        """
        Setter for the Type argument.
        type: str: The type of test data to create, e.g., "address", "user_data", etc. Currently supporting: "address".
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Type. Changing Type from `{self.type}` to `{type}`")
        self.type = type

    @keyword
    def set_amount(self, amount: int = None):
        """
        Setter for the Amount argument.
        amount: int: The amount of rows of test data to generate.
        Default = 3.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Amount. Changing Amount from `{self.amount}` to `{amount}`")
        self.amount = amount

    @keyword
    def set_format(self, format: str = None):
        """
        Setter for the Format argument.
        format: str: The format in which the test data will be given. If None, will return a 2-dimensional list.
        Default = None.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Format. Changing Format from `{self.format}` to `{format}`")
        self.format = format

    @keyword
    def set_kwarg(self, argument, value = None):
        """
        Setter for Kwarg arguments. 
        Give the name of the kwarg argument and the value you want to set it to. 
        E.g., Set Kwarg    country    Czechia. 
        Set to None to unset it.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Kwarg. Changing Kwarg `{argument}` to `{value}`")
        self.kwargs[argument] = value