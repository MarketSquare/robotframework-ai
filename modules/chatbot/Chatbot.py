from robot.api.deco import keyword, library

from modules.Module import Module


@library
class Chatbot(Module):
    def __init__(self) -> None:
        super().__init__("chatbot")
        self.history = []

    @keyword
    def generate_response(
            self,
            ai_model:str,
            message:str,
            model:str=None,
            max_tokens:int=256,
            temperature:float=1,
            top_p:float=1,
            frequency_penalty:float=0,
            presence_penalty:float=0,
            keep_history:bool = False,
            response_format:dict = None
        ):
        """        
        Chatbot
        =======


        Chatbot_ is a simple response generating library for `Robot Framework`_ similar to
        ChatGPT on the web. You can ask it a question or give it a task to have it automatically
        reply to your emails.


        Functionality
        =============

        The following parameters can be used (parameters with a * are required):
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

        The RealTestDataGenerator can support multiple different AI models. Each AI model needs an API key for the generation of test data.
        Using the python library the key gets automatically read from a .env file. To use your key, create a .env file in the root directory
        and declare your key there. Each AI model has their own API key. To define a key, create a variable with the name of
        the AI model capitalized followed by "_KEY". Then set this variable to your key. 

        *Example .env file*

        OPENAI_KEY="278bxw4m89monwxmu89wm98ufx8hwxfhqwifmxou09qwxp09jmx"

        GEMINI_KEY="cavhjbcZCJKnvmzxcnzkcjkczckzcskjnjn7h38nwd923hdnind"
        """        
        self.validate_default_input_parameters(max_tokens, temperature, top_p, frequency_penalty, presence_penalty)
        message = self.create_message(message, keep_history)
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
        self.set_history(prompt, response, keep_history)
        return response.message

    def create_message(self, message:str, keep_history:bool):
        if keep_history:
            return self.history + [{"role": "user", "content": message}]
        return [{"role": "user", "content": message}]
    
    def set_history(self, prompt:object, response:object, keep_history:bool):
        if not keep_history:
            self.history = []
        self.history += prompt.message + [{"role": "assistant", "content": response.message}]
