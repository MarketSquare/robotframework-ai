=====================
RealTestDataGenerator
=====================


.. default-role:: code


RealTestDataGenerator_ is a test data generating library for `Robot Framework`_ similar to
 the library Faker_. This library however generates real existing data, using AI.



Functionality
=============

To generate test data simply import the package and use the keyword: Generate Test Data
This keyword takes various parameters, some being specific for the generation of certain
types of test data.

The following parameters can be used (parameters in bold are required):
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
- *presence_penalty:float:* Exact same as frequency_penalty except its scope is reduced to the immidiate context.
    Can be anything from -2 to 2. Default = 0
- *kwargs:dict:* Additional parameters can be supplied for specific types of test data. These will be explained in per type below

Addresses
---------

When generating addresses additional parameter are available. These parameters are as follows:
- *Country:str:* The country from which to create addresses. If None, will generate an address from anywhere. Default = None
