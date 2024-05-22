=================
RobotFramework-AI
=================


.. default-role:: code


RobotFramework-AI_ is a library that adds AI functionality to the `Robot Framework`_.
It can generate test data for you using the RealTestDataGenerator_ but also answer your
questions with the Chatbot_. 


RealTestDataGenerator
=====================

RealTestDataGenerator_ can generate test data for the `Robot Framework`_ similar to
the library Faker_. The RealTestDataGenerator however generates real existing data, using AI.

To generate test data simply import the package and use the keyword: Generate Test Data
This keyword takes various arguments, some being specific for the generation of certain
types of test data.

The following arguments can be used (arguments in bold are required):
- **ai_model:str:** The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
- **type:str:** The type of test data to create, e.g. "address", "user_data", etc. Currently supporting: "address"
- *amount:int:* The amount of rows of test data to generate. Default = 3
- *format:str:* The format in which the test data will be given. If None, will return a 2 dimensional list. Default = None
- *max_tokens:int:* The token limit for a conversation. Both prompt and response tokens will count towards this limit. Default = 256
- *model:str:* AI model specfic. The model of the AI model to be used. E.g. "gpt-3.5-turbo" when using the "openai" AI model.
    Default per AI model:
        - "openai" = "gpt-3.5-turbo"
- *temperature:float:* This value determines the creativity of the AI model. Can be anything from 0-2. Default = 1
- *top_p:float:* Similar to temperature. Determines the selection of tokens before selecting one.
    The higher the value the more less common tokens get added to the selection. Can be anything from 0-2. Default = 1
- *frequency_penalty:float:* Penalizes more frequent token reducing the chance of it reappearing.
    Negative values encourage it to reuse tokens. Can be anything from -2 to 2. Default = 0
- *presence_penalty:float:* Exact same as frequency_penalty except its scope is reduced to the immediate context.
    Can be anything from -2 to 2. Default = 0
- *kwargs:dict:* Additional arguments can be supplied for specific types of test data. These will be explained in per type below

Addresses
---------

When generating addresses additional argument are available. These arguments are as follows:
- *Country:str:* The country from which to create addresses. If None, will generate an address from anywhere. Default = None


Chatbot
=======

Chatbot_ is a simple response generating library for `Robot Framework`_ similar to
ChatGPT on the web. You can ask it a question or give it a task to have it automatically
reply to your emails.

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
In the case of kwargs, use the setter to set individual kwargs, set to None to unset it. The setter takes 2 arguments, the name of
the kwarg to set and its value.
To set a kwarg use: Set Kwarg    country    Czechia
