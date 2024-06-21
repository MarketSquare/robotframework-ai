from robot.api.deco import keyword, library
from RobotFrameworkAI.ai_interface.AI_Interface import AI_Interface
from RobotFrameworkAI.objects.prompt.Prompt import Prompt
from RobotFrameworkAI.objects.prompt.PromptConfig import PromptConfig
from RobotFrameworkAI.objects.prompt.PromptMetadata import PromptMetadata
import logging


logger = logging.getLogger(__name__)


@library
class Module:
    """
    The interface for all modules.

    A module is a class containing keywords for the Robot Framework to use.
    They use AI to perform the task they are intended to do.
    This can be the generation of test data or just a simple chatbot that answers your questions.

    In this base class for modules common code is shared. This includes the creation of Prompt objects and
    the validation and the setting of common arguments.

    The setters can be used to set the defaut values for the arguments for each keyword.
    All attributes and setters here are common arguments and are shared between every module.
    This also means that setting these arguments will set them for every module.

    To create a new module, create a new folder in the modules folder for all its logic.
    Create a keyword that atleast accepts all these arguments and uses the get_default_values_for_common_arguments
    method to set the values of each argument incase they are not given.
    Make sure each arguments defaults to None so the setters can take effect.
    
    Call the create_prompt method to create a Prompt and use this with the send_prompt method from the AI_Interface.
    This wil return a Response which then needs to be structured in the way the users of the module expect it.

    NOTE: When creating a package all module will get inherited by the RobotFrameworkAI library. This way all
    keywords and methods will be available. An anoying side effect of this is that methods in seperate classes
    but with the same name will both be available. This causes only the method of the first inherited class to
    be available.
    """

    def __init__(self) -> None:
        self.ai_interface = AI_Interface()
        self.name = "base_module"
        self.ai_model = None
        self.model = None
        self.max_tokens = 256
        self.temperature = 1
        self.top_p = .5
        self.frequency_penalty = 0
        self.presence_penalty = 0
        self.response_format = None

    def create_prompt(
            self,
            ai_model:str,
            message:list[dict],
            model:str,
            max_tokens:int,
            temperature:float,
            top_p:float,
            frequency_penalty:float,
            presence_penalty:float,
            response_format:dict
        ) -> Prompt:
        config = PromptConfig(ai_model, model, response_format)
        arguments = {
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty
        }
        metadata = PromptMetadata(self.name)
        prompt = Prompt(
            config,
            message,
            arguments,
            metadata
        )
        return prompt

    def get_default_values_for_common_arguments(
            self,
            ai_model: str,
            model: str,
            max_tokens: int,
            temperature: float,
            top_p: float,
            frequency_penalty: float,
            presence_penalty: float,
            response_format: dict
        ):
        # Set defaut values for arguments
        ai_model = ai_model if ai_model is not None else self.ai_model
        model = model if model is not None else self.model
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens
        temperature = temperature if temperature is not None else self.temperature
        top_p = top_p if top_p is not None else self.top_p
        frequency_penalty = frequency_penalty if frequency_penalty is not None else self.frequency_penalty
        presence_penalty = presence_penalty if presence_penalty is not None else self.presence_penalty
        response_format = response_format if response_format is not None else self.response_format
        return ai_model, model, max_tokens, temperature, top_p, frequency_penalty, presence_penalty, response_format

    def validate_common_input_arguments(self, temperature:float, top_p:float, frequency_penalty:float, presence_penalty:float):
        error_messages = []
        if not self.is_valid_temperature(temperature):
            error_messages.append(f"Invalid value `{temperature}` for `temperature`. Value must be between 0 and 2 (inclusive).")
        if not self.is_valid_top_p(top_p):
            error_messages.append(f"Invalid value `{top_p}` for `top_p`. Value must be between 0 and 1 (inclusive).")
        if not self.is_valid_frequency_penalty(frequency_penalty):
            error_messages.append(f"Invalid value `{frequency_penalty}` for `frequency_penalty`. Value must be between -2 and 2 (inclusive).")
        if not self.is_valid_presence_penalty(presence_penalty):
            error_messages.append(f"Invalid value `{presence_penalty}` for `presence_penalty`. Value must be between -2 and 2 (inclusive).")

        if error_messages:
            error_message = f"Invalid input argument(s): {' '.join(error_messages)}"
            logger.error(error_message)
            raise ValueError(error_message)
        return True

    def is_valid_temperature(self, temperature:float):
        return 0 <= temperature <= 2
    def is_valid_top_p(self, top_p:float):
        return 0 <= top_p <= 2
    def is_valid_frequency_penalty(self, frequency_penalty:float):
        return -2 <= frequency_penalty <= 2
    def is_valid_presence_penalty(self, presence_penalty:float):
        return -2 <= presence_penalty <= 2

    # Setters
    @keyword
    def set_ai_model(self, ai_model: str):
        """
        Setter for the AI Model argument.
        ai_model: str: The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai".
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set AI Model. Changing AI Model from `{self.ai_model}` to `{ai_model}`")
        self.ai_model = ai_model

    @keyword
    def set_model(self, model: str):
        """
        Setter for the Model argument.
        model: str: AI model specific. The model of the AI model to be used, e.g., "gpt-3.5-turbo" when using the "openai" AI model.
        Default per AI model:
            - "openai" = "gpt-3.5-turbo"
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Model. Changing Model from `{self.model}` to `{model}`")
        self.model = model

    @keyword
    def set_max_tokens(self, max_tokens: int):
        """
        Setter for the Max Tokens argument.
        max_tokens: int: The token limit for a conversation. Both prompt and response tokens will count towards this limit.
        Default = 256.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Max Tokens. Changing Max Tokens from `{self.max_tokens}` to `{max_tokens}`")
        self.max_tokens = max_tokens

    @keyword
    def set_temperature(self, temperature: float):
        """
        Setter for the Temperature argument.
        temperature: float: This value determines the creativity of the AI model. Can be anything from 0-2.
        Default = 1.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Temperature. Changing Temperature from `{self.temperature}` to `{temperature}`")
        self.temperature = temperature

    @keyword
    def set_top_p(self, top_p: float):
        """
        Setter for the Top P argument.
        top_p: float: Similar to temperature. Determines the selection of tokens before selecting one.
        The higher the value, the more less likely tokens get added to the selection. Can be anything from 0-2. At 1,
        only the top 50% of tokens will be used when selecting a token; at 0, all tokens will be taken into consideration.
        Default = 1.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Top P. Changing Top P from `{self.top_p}` to `{top_p}`")
        self.top_p = top_p

    @keyword
    def set_frequency_penalty(self, frequency_penalty: float):
        """
        Setter for the Frequency Penalty argument.
        frequency_penalty: float: Penalizes more frequent tokens, reducing the chance of them reappearing.
        Negative values encourage reuse of tokens. Can be anything from -2 to 2.
        Default = 0.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Frequency Penalty. Changing Frequency Penalty from `{self.frequency_penalty}` to `{frequency_penalty}`")
        self.frequency_penalty = frequency_penalty

    @keyword
    def set_presence_penalty(self, presence_penalty: float):
        """
        Setter for the Presence Penalty argument.
        presence_penalty: float: Similar to frequency_penalty but its scope is reduced to the immediate context.
        The immediate context can be seen as one or more paragraphs about a singular subject.
        Can be anything from -2 to 2.
        Default = 0.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Presence Penalty. Changing Presence Penalty from `{self.presence_penalty}` to `{presence_penalty}`")
        self.presence_penalty = presence_penalty

    @keyword
    def set_response_format(self, response_format: dict):
        """
        Setter for the Response Format argument.
        response_format: dict: Can be used to make the response compile to JSON.
        Set this to { "type": "json_object" } to make the response compile to JSON or None if it shouldn't necessarily.
        Default = None.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Response Format. Changing Response Format from `{self.response_format}` to `{response_format}`")
        self.response_format = response_format