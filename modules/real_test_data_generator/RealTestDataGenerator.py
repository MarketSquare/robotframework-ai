from robot.api.deco import keyword, library

from modules.Module import Module
from modules.real_test_data_generator.test_data_generators.AddressGenerator import AddressGenerator
from modules.real_test_data_generator.test_data_generators.UserDataGenerator import UserDataGenerator


@library
class RealTestDataGenerator(Module):    
    # Robot library stuff
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_VERSION = "1"

    def __init__(self) -> None:
        super().__init__("real_test_data_generator")
        self.generators = {
            "address": AddressGenerator(),
            "user_data": UserDataGenerator(),
        }
        
    
    @keyword
    def generate_test_data(
            self,
            ai_model:str,
            type:str,
            model:str=None,
            amount:int=3,
            format:str=None,
            max_tokens:int=256,
            temperature:float=1,
            top_p:float=1,
            frequency_penalty:float=0,
            presence_penalty:float=0,
            response_format:dict={ "type": "json_object" },
            **kwargs
        ):
        """
        
        RealTestDataGenerator
        =====================


        RealTestDataGenerator_ is a test data generating library for `Robot Framework`_ similar to
        the library `Faker`_. This library however generates real existing data, using AI.


        Functionality
        =============

        The following parameters can be used (parameters with a * are required):
        - *ai_model: str: The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
        - *type: str: The type of test data to create, e.g. "address", "user_data", etc. Currently supporting: "address"
        - model: str: AI model specfic. The model of the AI model to be used. E.g. "gpt-3.5-turbo" when using the "openai" AI model.
            Default per AI model:
                - "openai" = "gpt-3.5-turbo"
        - amount: int: The amount of rows of test data to generate. Default = 3
        - format: str: The format in which the test data will be given. If None, will return a list. Default = None
        - max_tokens: int: The token limit for a conversation. Both prompt and response tokens will count towards this limit. Default = 256
        - temperature: float: This value determines the creativity of the AI model. Can be anything from 0-2. Default = 1
        - top_p: float: Similar to temperature. Determines the selection of tokens before selecting one.
            The higher the value the more less likely tokens get added to the selection. Can be anything from 0-2. At 1,
            only the top 50% of tokens will be used when selecting a token at 0 all tokens will be taken into consideration. Default = 1
        - frequency_penalty: float: Penalizes more frequent token reducing the chance of it reappearing.
            Negative values encourage it to reuse tokens. Can be anything from -2 to 2. Default = 0
        - presence_penalty: float: Exact same as frequency_penalty except its scope is reduced to the immediate context.
            The immediate context can be seen as one or more paragrahps about a singular subject.
            Can be anything from -2 to 2. Default = 0
        - response_format: dict: Can be used to make the response compile to JSON.
            Set this to { "type": "json_object" } to make the response compile to JSON or None if it shouldn't necessarily.
            Default = { "type": "json_object" }
        - kwargs: dict: Additional parameters can be supplied for specific types of test data. These will be explained per type below

        *Addresses*
        ---------

        When generating addresses additional parameter are available. These parameters are as follows:
        - Country: str: The country from which to create addresses. If None, will generate an address from anywhere. Default = None


        AI models
        =========

        The RealTestDataGenerator can support multiple different AI models. Each AI model needs an API key for the generation of test data.
        Using the python library the key gets automatically read from a .env file. To use your key, create a .env file in the root directory
        and declare your key there. Each AI model has their own API key. To define a key, create a variable with the name of
        the AI model capitalized followed by "_KEY". Then set this variable to your key. 

        *Example .env file*

        OPENAI_KEY="278bxw4m89monwxmu89wm98ufx8hwxfhqwifmxou09qwxp09jmx"

        GEMINI_KEY="cavhjbcZCJKnvmzxcnzkcjkczckzcskjnjn7h38nwd923hdnind"
        """
        self.validate_default_input_parameters(max_tokens, temperature, top_p, frequency_penalty, presence_penalty)
        self.validate_module_specific_parameters(type)
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


    def validate_module_specific_parameters(self, type:str):
        error_messages = []        
        if not self.is_valid_type(type):
            error_messages.append(f"Invalid value '{type}' for 'type'. Value must be in: {', '.join(self.generators.keys())}.")
        if error_messages:
            raise ValueError("\n".join(error_messages))

    def is_valid_type(self, type:str):
        return type in self.generators