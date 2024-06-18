from robot.api.deco import keyword, library

from RobotFrameworkAI.modules.Module import Module
from RobotFrameworkAI.modules.real_test_data_generator.test_data_generators.AddressGenerator import AddressGenerator
from RobotFrameworkAI.modules.real_test_data_generator.test_data_generators.UserDataGenerator import UserDataGenerator
import logging


logger = logging.getLogger(__name__)


@library
class RealTestDataGenerator(Module):
    """
    The RealTestDataGenerator is a module that generates real test data.

    The test data is real in the sense that it can or could (depending on the type of test data)
    exist in the real world. In the case of addresses, the generated addresses should exists, and
    thus should be findable on for example Google maps.

    The aim om this module is to overcome the issues the library Faker has.
    So if Faker can already generate has no issues generating email addresses, then the
    RealTestDataGenerator wont implement this logic.
    """
    def __init__(self) -> None:
        super().__init__()
        self.name = "real_test_data_generator"
        self.generators = {
            "address": AddressGenerator(),
            "user_data": UserDataGenerator(),
        }
        self.type = None
        self.amount = 3
        self.format = None
        self.response_format = None
        self.kwargs = {}

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
        logger.debug(f"Calling keyword: Generate Test Data with arguments: (ai_model: {ai_model}), (type: {type}), (model: {model}), (amount: {amount}), (format: {format}), (max_tokens: {max_tokens}), (temperature: {temperature}), (top_p: {top_p}), (frequency_penalty: {frequency_penalty}), (presence_penalty: {presence_penalty}), (response_format: {response_format}), (kwargs: {kwargs})")
        # Set defaut values for arguments
        argument_values = self.get_default_values_for_common_arguments(
            ai_model, model, max_tokens, temperature, top_p, frequency_penalty, presence_penalty, response_format
        )
        ai_model, model, max_tokens, temperature, top_p, frequency_penalty, presence_penalty, response_format = argument_values
        response_format = {"type": "json_object"}
        type, amount, format, kwargs = self.get_default_values_for_real_test_data_generator_specifc_arguments(type, amount, format, kwargs)

        if ai_model is None or type is None:
            error_message = f"Both ai_model and type are required and can't be None. AI model: `{ai_model}`, Type: `{type}`"
            logger.error(error_message)
            raise ValueError(error_message)

        self.validate_common_input_arguments(temperature, top_p, frequency_penalty, presence_penalty)
        self.validate_module_specific_arguments(type)
        generator = self.generators[type]
        message = generator.create_prompt_message(amount, format, kwargs)
        prompt = self.create_prompt(
            ai_model,
            message,
            model,
            max_tokens,
            temperature,
            top_p,
            frequency_penalty,
            presence_penalty,
            response_format
        )
        response = self.ai_interface.send_prompt(prompt)
        response = generator.format_response(response)
        return response

    def get_default_values_for_real_test_data_generator_specifc_arguments(self, type:str, amount:int, format:str, kwargs:dict):
        type = type if type is not None else self.type
        amount = amount if amount is not None else self.amount
        format = format if format is not None else self.format

        # Do the same but for kwargs arguments
        for key, value in self.kwargs.items():
            if key not in kwargs and value is not None:
                kwargs[key] = value
        return type, amount, format, kwargs

    def validate_module_specific_arguments(self, type:str):
        error_messages = []        
        if not self.is_valid_type(type):
            error_messages.append(f"Invalid value '{type}' for 'type'. Value must be in: {', '.join(self.generators.keys())}.")

        if error_messages:
            error_message = f"Invalid input argument(s): {' '.join(error_messages)}"
            logger.error(error_message)
            raise ValueError(error_message)
        return True

    def is_valid_type(self, type:str):
        return type in self.generators
    
    # Setters
    @keyword
    def set_type(self, type: str):
        """
        Setter for the Type argument.
        type: str: The type of test data to create, e.g., "address", "user_data", etc. Currently supporting: "address".
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Type. Changing Type from `{self.type}` to `{type}`")
        self.type = type

    @keyword
    def set_amount(self, amount: int):
        """
        Setter for the Amount argument.
        amount: int: The amount of rows of test data to generate.
        Default = 3.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Amount. Changing Amount from `{self.amount}` to `{amount}`")
        self.amount = amount

    @keyword
    def set_format(self, format: str):
        """
        Setter for the Format argument.
        format: str: The format in which the test data will be given. If None, will return a 2-dimensional list.
        Default = None.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Format. Changing Format from `{self.format}` to `{format}`")
        self.format = format

    @keyword
    def set_kwarg(self, argument, value):
        """
        Setter for Kwarg arguments. 
        Give the name of the kwarg argument and the value you want to set it to. 
        E.g., Set Kwarg    country    Czechia. 
        Set to None to unset it.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Kwarg. Changing Kwarg `{argument}` to `{value}`")
        self.kwargs[argument] = value