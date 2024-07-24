
# RobotFramework-AI

`RobotFramework-AI` is a library that adds AI functionality to the `Robot Framework`.
It can generate test data for you using the `RealTestDataGenerator` but also reply to your
messages with the `Chatbot`.

## Setup

To setup the library:

1. Start by cloning this repository.
2. Open a terminal and locate the `robotframework-ai` folder.
3. Use the following command to create the package.

        python setup.py sdist bdist_wheel

    This requires the wheel package to be installed, which can be installed with:

        pip install wheel

4. To install the library using the package just created, use the following command.

        pip install .\dist\RobotFrameworkAI-0.0.2-py3-none-any.whl

5. Setup the API key for the AI you want to use. This can be done by creating a new environment variable called `OPENAI_KEY` with your key as the value. More information about this in the AI models header below.
6. The library is now properly setup, to confirm it works, run the following code in a robot file. This will generate 3 addresses and create a log.html file.

        *** Settings ***
        Library   RobotFrameworkAI


        *** Test Cases ***
        Exec Test
            [Documentation]    Test
            ${response}    Generate Test Data    openai    address
            Log    ${response}

    Opening this testlog file in a browser and opening the suite `Test`, the test `Exec test` and the keyword `Log` will reveal a list with the 3 addresses in the `INFO` section.

    ![testlog](https://github.com/user-attachments/assets/b97ade59-0156-4817-aff1-555637eddcd1)

## AI models

Each module in the RobotFramework-AI library can support multiple different AI models. Each AI model needs an API key for the generation of test data.
This key gets read directly from your environment variables. Each AI model has their own API key. To define a key, create a new variable with the name of
the AI model capitalized followed by "_KEY". Then set this variable to your key. At the moment only OpenAI is supported.

**Example API keys**
- OPENAI_KEY=278bxw4m89monwxmu89wm98ufx8hwxfhqwifmxou09qwxp09jmx
- GEMINI_KEY=cavhjbcZCJKnvmzxcnzkcjkczckzcskjnjn7h38nwd923hdnind

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

## Chatbot

The `Chatbot` is a simple response generating library for `Robot Framework` similar to
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

## Assistant

The `Assistant` is a module that allows talking to AI and adding files to the conversation.

It functions similar to the Chatbot module, but with some changes.
With the `Assistant` module AI Assistants can be created, these will exists for aslong as they
are not deleted, meaning that they are still available several weeks later or indefinitely.
In the mean time new AI Assistants can be created and talked to.

Files can be uploaded to the AI for inspection or to add knowledge. Similarly files can also
be send along side a message to the AI Assistant. The difference being that files send alongsides
message only remain aslong as the thread (conversation). When a new thread is created,
the AI Assistant wont remember previous message send to it, including files. It will only
remember files uploaded to the AI assistant itself.

The `Assistant` can also be given instructions and parameters to influence its behaviour. These
can be given at creation or later be changed.

### Keywords

The `Assistant` has 9 different keywords that can be used to interact with the AI assistant.
The way the `Assistant` module works is that there can be multiple AI assistants. But there can
only be 1 active assistant. All keywords where it isn't explicitely mentioned which assistant
will be affected (all keywords that don't require an Id as argument), will be performed on the
active assistant.

#### Create Assistant

This keyword creates a new assistant and sets it as the active assistant.

Returns the Id of the newly created assistant.

The following arguments can be used (arguments prefixed by an * are required):

- ***ai_model: str:** The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
- ***name: str:** The name of the assistant. This name will show up in responses and in the logs, e.g. "Bob". Max 256 characters
- ***instructions: str:** The instructions given to the assistant. Here you can explain how the assistant should behave, e.g. "You are a software engineer that can debug my code and explain it in a easy to understand manner". Max 256,000 characters
- **model: str:** AI model specfic. The model of the AI model to be used. E.g. "gpt-3.5-turbo" when using the "openai" AI model. Default depends on AI model:
  - "openai" = "gpt-3.5-turbo"
- **temperature: float = 1** This value determines the creativity of the AI model. Can be anything from 0-2.
- **top_p: float = 1** Similar to temperature. Determines the selection of tokens before selecting one. The higher the value the more less likely tokens get added to the selection. Can be anything from 0-2. At 1, only the top 50% of tokens will be used when selecting a token at 0 all tokens will be taken into consideration
- **response_format: dict = None** Can be used to make the response compile to JSON. Set this to { "type": "json_object" } to make the response compile to JSON or None if it shouldn't necessarily.

##### Examples

Create a new assistant Test Assistant:

    Set AI Model    openai
    Set Name    Test Assistant
    Create Assistant

Create a new assistant with all changing all default arguments:

    Set AI Model    openai
    Set Name    Full Featured Assistant
    Set Instructions    This assistant is capable of handling various technical queries.
    Set Model    gpt-3.5-turbo
    Set Temperature    1.5
    Set Top P    0.8
    Set Response Format    { "type": "json_object" }
    Create Assistant

#### Update Assistant

This keyword updates parameters of the active assistant.

This keyword takes the same arguments as the Create Assistant keyword

Returns a success message explaining which parameters have been updated.

The following arguments can be used (arguments prefixed by an * are required):

- ***ai_model: str:** The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
- **name: str:** The name of the assistant. This name will show up in responses and in the logs, e.g. "Bob". Max 256 characters
- **instructions: str:** The instructions given to the assistant. Here you can explain how the assistant should behave, e.g. "You are a software engineer that can debug my code and explain it in a easy to understand manner". Max 256,000 characters
- **model: str:** AI model specfic. The model of the AI model to be used. E.g. "gpt-3.5-turbo" when using the "openai" AI model. Default depends on AI model:
  - "openai" = "gpt-3.5-turbo"
- **temperature: float = 1** This value determines the creativity of the AI model. Can be anything from 0-2.
- **top_p: float = 1** Similar to temperature. Determines the selection of tokens before selecting one. The higher the value the more less likely tokens get added to the selection. Can be anything from 0-2. At 1, only the top 50% of tokens will be used when selecting a token at 0 all tokens will be taken into consideration
- **response_format: dict = None** Can be used to make the response compile to JSON. Set this to { "type": "json_object" } to make the response compile to JSON or None if it shouldn't necessarily.

##### Examples

Update the active assistant's name:

    Set AI Model    openai
    Set Name    Mark
    Update Assistant

Update the all the parameters of the active assistant:

    Set AI Model    openai
    Set Name    Helpy
    Set Instructions    You write documentation for code.
    Set Model    gpt-3.5-turbo
    Set Temperature    1.8
    Set Top P    0.6
    Set Response Format    { "type": "json_object" }
    Update Assistant

#### Send Message

Sends a prompt to the active assistant and returns its response

By supplying file_paths as an argument in the method call, files can be send with it as well. Make sure to unset file_paths to not send it with each prompt.

The following arguments can be used (arguments prefixed by an * are required):

- ***ai_model: str:** The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
- ***message: str:** The message you want to send to the AI model, e.g. "What is the weather today?"
- ***file_paths: str:** A list of paths that determine which files get send with the prompt. Both paths to files and paths to folder can be used. Paths to files will directly add that file to the prompt. Paths to folders will look into all files in that folder and add them to the prompt. e.g. ["src/main.py", "src/resources"]
**NOTE:** file_paths can not be set using setters. Allowing file_paths to be set could cause users to accidentally add the same files multiple times to the same assistant and will also cause users to send those with every prompt. This would make the library slower but more importantly lose the user a lot of money.


##### Examples

Send a prompt to ask for the weather:

    Set AI Model    openai
    Set Message    What is the weather today?
    Send Message

Send a prompt to ask for improvements for code:

    Set AI Model    openai
    Set Message    How can I improve my code?
    Send Message    file_paths=["src/main.py", "src/resources"]

#### Delete Assistant

Deletes the active assistant

After deleting the active assistant, there will be no active assistant. Either create a new assistant or set a new assistant as active.

The following arguments can be used (arguments prefixed by an * are required):

- ***ai_model: str:** The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"

##### Examples

Delete the active assistant:

    Set AI Model    openai
    Delete Assistant

#### Delete Assistant By Id

Deletes the assistant with the specified Id

If that assistant is also the active assistant, there will be no active assistant. Either create a new assistant or set a new assistant as active.

The following arguments can be used (arguments prefixed by an * are required):

- ***ai_model: str:** The AI model to be used, e.g. "openai"
- ***id: str:** The Id of the assistant. This an Id created by the AI model itself. e.g. "asst_0Ta3aCdE675foHxkLTnujjgl"

##### Examples

Delete an assistant by Id:

    Set AI Model    openai
    Set Id    asst_0Ta3aCdE675foHxkLTnujjgl
    Delete Assistant By Id

#### Attach Files

Attaches files to the active assistant

These files can be used by the assistant in any thread as opposed to sending files with a prompt.

The following arguments can be used (arguments prefixed by an * are required):

- ***ai_model: str:** The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
- ***file_paths: str:** A list of paths that determine which files get send with the prompt. Both paths to files and paths to folder can be used. Paths to files will directly add that file to the prompt. Paths to folders will look into all files in that folder and add them to the prompt. e.g. ["src/main.py", "src/resources"]
**NOTE:** file_paths can not be set using setters. Allowing file_paths to be set could cause users to accidentally add the same files multiple times to the same assistant and will also cause users to send those with every prompt. This would make the library slower but more importantly lose the user a lot of money.

##### Examples

Attach the main.py file and all files in the src/resources directory:

    Set AI Model    openai
    Set File Paths    ["src/main.py", "src/resources"]
    Attach Files

#### Get Active Assistant Id

Returns the Id of the active assistant

The following arguments can be used (arguments prefixed by an * are required):

- ***ai_model: str:** The AI model to be used, e.g. "openai"

##### Examples

Get the Id of the active assistant using setters:

    Set AI Model    openai
    Get Active Assistant Id

#### Create New Thread

Create a new thread

Creating a new thread effectively restarts the conversation.

The following arguments can be used (arguments prefixed by an * are required):

- ***ai_model: str:** The AI model to be used, e.g. "openai"

##### Examples

Create a new thread using setters:

    Set AI Model    openai
    Create New Thread

#### Set Active Assistant

Sets the assistant with the specified Id as active

This will also create a new thread

The following arguments can be used (arguments prefixed by an * are required):

- ***ai_model: str:** The AI model to be used, e.g. "openai"
- ***id: str:** The Id of the assistant. This an Id created by the AI model itself. e.g. "asst_0Ta3aCdE675foHxkLTnujjgl"

##### Examples

Set a specific assistant as the active assistant and start a new thread using setters:

    Set AI Model    openai
    Set Id    asst_0Ta3aCdE675foHxkLTnujjgl
    Set Active Assistant


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

Each argument has its own setter, the name of the keyword is 'Set' plus the name of the argument e.g. Set AI Model for AI Model.
In the case of kwargs, use the setter to set individual kwargs, set to None to unset it. The setter takes 2 arguments, the name of
the kwarg to set and its value.
To set a kwarg use:

    Set Kwarg    country    Czechia

**NOTE:** file_paths can not be set using setters. Allowing file_paths to be set could cause users to accidentally add the same files multiple times to the same assistant and will also cause users to send those with every prompt. This would make the library slower but more importantly lose the user a lot of money.

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
