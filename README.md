
# RobotFramework-AI

`RobotFramework-AI` is a library that adds AI functionality to the `Robot Framework`.
It can generate test data for you using the `RealTestDataGenerator` but also reply to your
messages with the `Chatbot`.

## RealTestDataGenerator

`RealTestDataGenerator` can generate test data for the `Robot Framework` similar to
the library `Faker`. The `RealTestDataGenerator` however, generates real existing data, using AI.

To generate test data simply import the package and use the keyword: `Generate Test Data`
This keyword takes various arguments, some being specific for the generation of certain
types of test data.

The following arguments can be used (arguments prefixed by an * are required):

- ***ai_model: str:** The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
- ***type: str:** The type of test data to create, e.g. "address", "user_data", etc. Currently supporting: "address"
- **model: str:** AI model specfic. The model of the AI model to be used. E.g. "gpt-3.5-turbo" when using the "openai" AI model.
    Default per AI model:
  - "openai" = "gpt-3.5-turbo"
- **amount: int = 3** The amount of rows of test data to generate.
- **format: str = None** The format in which the test data will be given. If None, will return a 2 dimensional list.
- **max_tokens: int = 256** The token limit for a conversation. Both prompt and response tokens will count towards this limit.
- **temperature: float = 1** This value determines the creativity of the AI model. Can be anything from 0-2.
- **top_p: float = 1** Similar to temperature. Determines the selection of tokens before selecting one.
    The higher the value the more less likely tokens get added to the selection. Can be anything from 0-2. At 1,
    only the top 50% of tokens will be used when selecting a token at 0 all tokens will be taken into consideration
- **frequency_penalty: float = 0** Penalizes more frequent token reducing the chance of it reappearing.
    Negative values encourage it to reuse tokens. Can be anything from -2 to 2.
- **presence_penalty: float = 0** Exact same as frequency_penalty except its scope is reduced to the immediate context.
    The immediate context can be seen as one or more paragrahps about a singular subject.
    Can be anything from -2 to 2.
- **kwargs: dict:** Additional arguments can be supplied for specific types of test data. These will be explained in per type below

**NOTE:** Be careful with changing the temperature, top p, frequency- and presence penalty as it will likely deviate from the format we expect it to return.

### Addresses

When generating addresses additional argument are available. These arguments are as follows:

- **Country:str:** The country from which to create addresses. If None, will generate an address from anywhere. Default = None

### Examples

Generate 3 addresses from anywhere using OpenAI:

    Generate Test Data    openai    address

Generate 10 addresses from Finland using the gpt-3.5-turbo from OpenAI in the default format with a token limit at 1024, temperature at 1, top p at .5 and frequency- and presence penalty at 0

    Generate Test Data    openai    address    gpt-3.5-turbo    10    None    1024    1    .5    0    0    country=finland

### Phone Numbers
When generating phone numbers, additional arguments are available.
These arguments are as follows:
- **country: str:** The country on which the [number prefix](https://www.iban.com/dialing-codes) and phone format is based. If prefix or phone format are defined in kwargs, only country prefix value stays, but format is defined exactly by prefix and phone format. If None, will generate numbers from different countries around the world in international format. Default = None
- **prefix: str:** Prefix type for output phone numbers. Takes values either as example (+xxx, 00xxx...) or name of the format ('international'). If None, prefix is set to international '+xxx'. If phone_format is defined, prefix gets overriden. Default = None
- **phone_format: str:** Exact definition of phone format user wants to output e.g. 
(212)456-7890
+212-456-7890
212.456.7890
User can define prefix, dashes, spaces, parenthesses and other symbols if needed. Overrides prefix argument and keeps the country argument. If None, the format is either international or typical for the country that is specified via country argument. Default = None
- **mix_format: bool = False** Phone number format mixer. If set to True, generated list of phone numbers has different phone number formats and prefix types. If False, output list of numbers is in the same format. Default = False

### Examples
Generate 3 phone numbers from anywhere in the world in international phone number format without dashes or spaces using OpenAI:

    Generate Test Data    openai    phone_number 

    # Output: ['+819012345678', '+442071231234', '+33123456789'] 

Generate 10 phone numbers from Norway with phone format set to "0047 8765 4321", using the gpt-3.5-turbo from OpenAI in the default format with a token limit at 1024, temperature at 1, top p at .5 and frequency- and presence penalty at 0, 

    Generate Test Data    openai    phone_number    gpt-3.5-turbo    10    None    1024    1    .5    0    0    country=norway phone_format="0047 xxxx xxxx"

    # Output: ['0047 2198 7654', '0047 5432 1987', '0047 4567 8901', '0047 8765 4321', '0047 3210 9876', '0047 6543 2109', '0047 7890 6543', '0047 1098 7654', '0047 9876 5432', '0047 2345 6789']

Generate 10 phone numbers from around the world with mix_format = True

    Generate Test Data    openai    phone_number    mix_format = True

    #Output: //ADD OUTPUT WHEN BUG FIXED//




## Chatbot

`Chatbot` is a simple response generating library for `Robot Framework` similar to
`ChatGPT` on the web. You can ask it a question or give it a task to have it automatically
reply to your emails.

The following arguments can be used (arguments prefixed by an * are required):

- ***ai_model: str:** The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
- ***message: str:** The message you want to send to the AI model, e.g. "What is the weather today?"
- **model: str:** AI model specfic. The model of the AI model to be used. E.g. "gpt-3.5-turbo" when using the "openai" AI model.
    Default depends on AI model:
  - "openai" = "gpt-3.5-turbo"
- **max_tokens: int = 256** The token limit for a conversation. Both prompt and response tokens will count towards this limit.
- **temperature: float = 1** This value determines the creativity of the AI model. Can be anything from 0-2.
- **top_p: float = 1** Similar to temperature. Determines the selection of tokens before selecting one.
    The higher the value the more less likely tokens get added to the selection. Can be anything from 0-2.
    At 1, only the top 50% of tokens will be used when selecting a token at 0 all tokens will be taken into consideration
- **frequency_penalty: float = 0** Penalizes more frequent token reducing the chance of it reappearing.
    Negative values encourage it to reuse tokens. Can be anything from -2 to 2.
- **presence_penalty: float = 0** Exact same as frequency_penalty except its scope is reduced to the immediate context.
    The immediate context can be seen as one or more paragrahps about a singular subject.
    Can be anything from -2 to 2.
- **keep_history: bool = False** A flag to keep the chat history of previous messages. When settings this to True, your previous prompt and
    the response by the AI will be saved for the next message. This feature will keep the previous message, so if you want to send
    two messages and refer to your first message from the second message, you need to set this flag to True in the second message.
    Leaving this on for the third message aswell will keep both the first and second message.

    **NOTE:** This works by incorporating the previous messages into the prompt, this will charge you again for both the prompt and
    response. So leaving this on, could quickly drain all your tokens.

- **response_format: dict = None** Can be used to make the response compile to JSON.
    Set this to { "type": "json_object" } to make the response compile to JSON or None if it shouldn't necessarily.

### Examples

Generate a response to a question using OpenAI

    Generate Response    openai    What is the wheather today?

Declare a rule in the first message and refer to it in the second message

    Generate Response    openai    If I say water you say fire
    Generate Response    openai    Water    keep_history=True

Generate the meaning of life in a json format using the gpt-3.5-turbo from OpenAI in the default format with a token limit at 1024, temperature at 2, top p at .5 and frequency- and presence penalty at 0 without using the previous messages in the response.

    Generate Response    openai    What is the meaning of life? In json.    gpt-3.5-turbo    1024    2    .5    0    0    False    {"type": "json_object"}   

## AI models

Each module in the RobotFramework-AI library can support multiple different AI models. Each AI model needs an API key for the generation of test data.
This key gets read directly from your environment variables. Each AI model has their own API key. To define a key, create a new variable with the name of
the AI model capitalized followed by "_KEY". Then set this variable to your key.

**Example API keys**
OPENAI_KEY=278bxw4m89monwxmu89wm98ufx8hwxfhqwifmxou09qwxp09jmx
GEMINI_KEY=cavhjbcZCJKnvmzxcnzkcjkczckzcskjnjn7h38nwd923hdnind

## Setters

Instead of providing all arguments through this keyword, it is also possible to set each argument beforehand. This way, when making repeated calls, arguments
do not have to be supplied each time. After setting these arguments they will remain untill set again. When arguments are set and the keyword also has arguments
supplied, then the supplied arguments will take priority.

**NOTE:** Setting arguments will impact other modules aswell. This means that when setting the temperature to 2, that both the RealTestDataGenerator and the Chatbot
will use this temperature from then on. This is only the case when both modules share arguments, the arguments that are shared are as followed:

    ai_model, model, max_tokens, temperature, top_p,
    frequency_penalty, presence_penalty, response_format

Each argument has its own setter, the name of the keyword is 'set' plus the name of the argument e.g. Set AI Model for AI Model.
In the case of kwargs, use the setter to set individual kwargs, set to None to unset it. The setter takes 2 arguments, the name of
the kwarg to set and its value.
To set a kwarg use:

    Set Kwarg    country    Czechia

### Examples

Generate 3 addresses from anywhere using OpenAI:

    Set AI Model    openai
    Set Type    address
    Generate Test Data

Generate 10 addresses from Finland using the gpt-3.5-turbo from OpenAI in the default format with a token limit at 1024, temperature at 1, top p at .5 and frequency- and presence penalty at 0

    Set AI Model    openai
    Set Type    address
    Set Model    gpt-3.5-turbo
    Set Amount    10
    Set Format    None
    Set Max Tokens    1024
    Set Temperature    1
    Set Top P    .5
    Set Frequency Penalty    0
    Set Presence Penalty    0
    Set Kwarg    country    finland
    Generate Test Data

## Logging

The RobotFramework-AI library includes configurable logging capabilities to assist with debugging and monitoring. This logging setup ensures that log messages are handled appropriately, including support for Unicode characters.

### Enabling Logging

To enable logging, use the Setup Logging keyword provided by the RobotFramework-AI library. This keyword allows you to configure console and file logging, and to enable or disable logging as needed.

The Setup Logging keyword takes the following arguments:

- **enabled: bool = True** Determines whether logging should be turned on.
- **for_test: bool = False** Can be used to log logs to a different folder specific for test logs.
    Will log to the logs_test folder instead of logs if set to True.
- **console_logging: bool = True** Determines whether logs should be printed in the console.
- **file_logging: bool = True** Determines whether logs should be logged to a file.

### Examples

To log to both the console and a file:

    Setup Logging

To log for tests without console logging:

    Setup Logging    True    True    False
