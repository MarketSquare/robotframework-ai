from robot.api.deco import keyword, library

from RobotFrameworkAI.modules.Module import Module
import logging


logger = logging.getLogger(__name__)


@library
class Chatbot(Module):
    """
    The Chatbot is a simple request response module.

    You can ask questions to the Chatbot and it will give you an answer.
    By default, messages send to an AI model wont be saved. This means that it
    wont recall your previous messages. To have your previous messages saved,
    set the keep_history flag to True. This will send your message along with
    your previous message and the response to it. Setting this flag to True for
    multiple messages in a row will keep the history for as long as it was True.
    """
    def __init__(self) -> None:
        super().__init__()
        self.module_name = "chatbot"
        self.ai_tool = "text_generator"
        self.history = []
        # Set arguments
        self.system_message = None
        self.message = None
        self.keep_history = False
        self.response_format = None

    @keyword
    def generate_response(
            self,
            ai_model:str=None,
            system_message:str=None,
            message:str=None,
            model:str=None,
            max_tokens:int=None,
            temperature:float=None,
            top_p:float=None,
            frequency_penalty:float=None,
            presence_penalty:float=None,
            keep_history:bool = None,
            response_format:dict = None
        ):
        """
        Chatbot
        =======


        Chatbot_ is a simple response generating module for `Robot Framework`_ similar to
        ChatGPT on the web. You can ask it a question or give it a task to have it automatically
        reply to your emails.


        Functionality
        =============

        The following arguments can be used (arguments with a * are required):
        - *ai_model: str: The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
        - *message: str: The message you want to send to the AI model, e.g. "What is the weather today?"
        - model: str: AI model specfic. The model of the AI model to be used. E.g. "gpt-3.5-turbo" when using the "openai" AI model.
            Default per AI model:
                - "openai" = "gpt-3.5-turbo"
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
        - keep_history: bool: A flag to keep the chat history of previous messages. When settings this to True, your previous prompt and
            the response by the AI will be saved for the next message. This feature will keep the previous message, so if you want to send
            two messages and refer to your first message from the second message, you need to set this flag to True in the second message.
            Leaving this on for the third message aswell will keep both the first and second message. Default = False.

            *NOTE:* This works by incorporating the previous messages into the prompt, this will charge you again for both the prompt and
            response. So leaving this on, could quickly drain all your tokens.

        - response_format: dict: Can be used to make the response compile to JSON.
            Set this to { "type": "json_object" } to make the response compile to JSON or None if it shouldn't necessarily.
            Default = { "type": "json_object" }

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

        # Set defaut values for arguments
        # If arguments are not given directly, get its default value. This is the value of the class attribute with the same name
        ai_model, system_message, message, model, max_tokens, temperature, top_p, frequency_penalty, presence_penalty, keep_history, response_format = self.get_default_values_for_arguments(
            ai_model = ai_model,
            system_message = system_message,
            message = message,
            model = model,
            max_tokens = max_tokens,
            temperature = temperature,
            top_p = top_p,
            frequency_penalty = frequency_penalty,
            presence_penalty = presence_penalty,
            keep_history = keep_history,
            response_format = response_format
        )
        # Log the arguments
        args = locals()
        args.pop("self")
        logger.debug(f"Calling keyword `Generate Response` with arguments: {', '.join(f'({k}: {v})' for k, v in args.items())}")
        # Validate arguments
        self.validate_input_arguments(
            message = message,
            max_tokens = max_tokens,
            temperature = temperature,
            top_p = top_p,
            frequency_penalty = frequency_penalty,
            presence_penalty = presence_penalty
        )
        history = self.history if keep_history else None
        prompt = self.create_prompt(
            self.ai_tool,
            ai_model,
            system_message,
            message,
            history,
            model,
            max_tokens,
            temperature,
            top_p,
            frequency_penalty,
            presence_penalty,
            response_format           
        )
        response = self.ai_interface.call_ai_tool(prompt)
        self.set_history(prompt, response, keep_history)
        return response.message

    def set_history(self, prompt:object, response:object, keep_history:bool):
        if not keep_history:
            self.history = []
        self.history.append({"user": prompt.message.user})
        self.history.append({"assistant": response.message})

    # Setters
    @keyword
    def set_system_message(self, system_message: str = None):
        """
        Setter for the System Message argument.
        system_message: str: The instruction for the AI model, e.g., "You are a helpful assistant.".
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set System Message. Changing System Message from `{self.system_message}` to `{system_message}`")
        self.system_message = system_message

    @keyword
    def set_keep_history(self, keep_history: bool = None):
        """
        Setter for the Keep History argument.
        keep_history: bool: A flag to keep the chat history of previous messages. When setting this to True, your previous prompt and
        the response by the AI will be saved for the next message. This feature will keep the previous message, so if you want to send
        two messages and refer to your first message from the second message, you need to set this flag to True in the second message.
        Leaving this on for the third message as well will keep both the first and second messages. Default = False.
        
        NOTE: This works by incorporating the previous messages into the prompt, this will charge you again for both the prompt and
        response. So leaving this on could quickly drain all your tokens.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Keep History. Changing Keep History from `{self.keep_history}` to `{keep_history}`")
        self.keep_history = keep_history