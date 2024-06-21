from robot.api.deco import keyword, library
from RobotFrameworkAI.modules.Module import Module
import logging

from RobotFrameworkAI.objects.prompt.ai_tool_data.AssistantData import AssistantData


logger = logging.getLogger(__name__)

class Assistant(Module):
    """
    The Assistant is a module that allows talking to AI and adding files to the conversation

    It functions similar to the Chatbot module, but with some changes.
    With the Assistant module AI assistants can be created, these will exists for aslong as they
    are not deleted, meaning that they are still available several weeks later or indefinitely.
    In the mean time new AI assistants can be created and talked to.

    Using the Attach Files keyword, files can be uploaded to the AI. Similarly files can also
    be send along side a message to the AI assistant. The difference being that files send alongsides
    message only remain aslong as the thread (conversation). When a new thread is created,
    the AI assistant wont remember previous message send to it, including files. It will only
    remember files attached to it.

    The assistant can be given instructions and parameters to influence its behaviour. These
    can be given at creation or later be changed using the Update Assistant keyword.
    """
    def __init__(self) -> None:
        super().__init__()
        self.module_name = "assistant"
        self.ai_tool = "assistant"
        # Setters
        self.id = None
        self.name = None
        self.message = None
        self.instructions = None

    def make_assistant_call(
            self,
            action: str,
            ai_model: str = None,
            name: str = None,
            model: str = None,
            temperature: float = None,
            top_p: float = None,
            response_format: dict = None,
            id: str = None,
            message: str = None,
            instructions: str = None,
            file_paths: list[str] = None
    ):
        """
        This method functions as base method for the keywords, containing common logic shared between all keywords (besides setters)

        This method creates the prompt, sends it to the AI interface and returns the result.
        """
        ai_tool_data = AssistantData(action, id, name, instructions, file_paths)
        # Max token, frequency penalty and presence penalty are not available for assistants and are set to None
        prompt = self.create_prompt(
            self.ai_tool,
            ai_model,
            None,
            message,
            None,
            model,
            None,
            temperature,
            top_p,
            None,
            None,
            response_format,
            ai_tool_data
        )
        response = self.ai_interface.call_ai_tool(prompt)
        return response

    @keyword
    def create_assistant(
            self,
            ai_model: str = None,
            name: str = None,
            instructions: str = None,
            model: str = None,
            temperature: float = None,
            top_p: float = None,
            response_format: dict = None
    ):
        """
        Creates a new assistant and returns its Id

        This new assistant will become the active assistant and a new thread will be created.
        
        The following arguments can be used (arguments with a * are required):
        - *ai_model: str: The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
        - *name: str: The name of the assistant. This name will show up in responses and in the logs, e.g. "Bob". Max 256 characters
        - *instructions: str: The instructions given to the assistant. Here you can explain how the assistant should behave,
            e.g. "You are a software engineer that can debug my code and explain it in a easy to understand manner". Max 256,000 characters
        - model: str: AI model specfic. The model of the AI model to be used. E.g. "gpt-3.5-turbo" when using the "openai" AI model.
            Default per AI model:
                - "openai" = "gpt-3.5-turbo"
        - temperature: float: This value determines the creativity of the AI model. Can be anything from 0-2. Default = 1
        - top_p: float: Similar to temperature. Determines the selection of tokens before selecting one.
            The higher the value the more less likely tokens get added to the selection. Can be anything from 0-2. At 1,
            only the top 50% of tokens will be used when selecting a token at 0 all tokens will be taken into consideration. Default = 1
        - response_format: dict: Can be used to make the response compile to JSON.
            Set this to { "type": "json_object" } to make the response compile to JSON or None if it shouldn't necessarily.
            Default = { "type": "json_object" }
        """
        action = "create_assistant"
        # If arguments are not given directly, get their default value. This is the value of the class attribute with the same name
        ai_model, name, instructions, model, temperature, top_p, response_format = self.get_default_values_for_arguments(
            ai_model=ai_model,
            name=name,
            instructions=instructions,
            model=model,
            temperature=temperature,
            top_p=top_p,
            response_format=response_format
        )
        # Log the arguments
        args = locals()
        args.pop("self")
        logger.debug(f"Calling keyword `Create Assistant` with arguments: {', '.join(f'({k}: {v})' for k, v in args.items())}")
        # Validate arguments
        self.validate_input_arguments(name=name, instructions=instructions, temperature=temperature, top_p=top_p)
        response = self.make_assistant_call(action, ai_model=ai_model, name=name, instructions=instructions, model=model, temperature=temperature, top_p=top_p, response_format=response_format)
        return response.message

    @keyword
    def send_message(self, ai_model: str = None, message: str = None, file_paths: list = None):
        """
        Sends a prompt to the active assistant and returns its response

        By supplying file_paths as an argument in the method call, files can be send with it aswell.
        Make sure to unset file_paths to not send it with each prompt.

        The following arguments can be used (arguments with a * are required):
        - *ai_model: str: The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
        - *message: str: The message you want to send to the AI model, e.g. "What is the weather today?"
        - file_paths: str: A list of paths that determine which files get send with the prompt.
            Both paths to files and paths to folder can be used. Paths to files will directly add that file to the prompt.
            Paths to folders will look into all files in that folder and add them to the prompt.
            e.g. ["src/main.py", "src/resources"]
        """
        action = "send_message"
        # If arguments are not given directly, get their default value. This is the value of the class attribute with the same name
        ai_model, message = self.get_default_values_for_arguments(ai_model=ai_model, message=message)
        # Log the arguments
        args = locals()
        args.pop("self")
        logger.debug(f"Calling keyword `Send Message` with arguments: {', '.join(f'({k}: {v})' for k, v in args.items())}")
        # Validate arguments
        self.validate_input_arguments(message=message)
        
        response = self.make_assistant_call(action, ai_model=ai_model, message=message, file_paths=file_paths)
        return response.message

    @keyword
    def delete_assistant(self, ai_model: str = None):
        """
        Deletes the active assistant

        After deleting the active assistant, there will be no active assistant.
        Either create a new assistant or set a new assistant as active.

        The following arguments can be used (arguments with a * are required):
        - *ai_model: str: The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
        """
        action = "delete_assistant"
        # If arguments are not given directly, get their default value. This is the value of the class attribute with the same name
        ai_model, = self.get_default_values_for_arguments(ai_model=ai_model)
        # Log the arguments
        args = locals()
        args.pop("self")
        logger.debug(f"Calling keyword `Delete Assistant` with arguments: {', '.join(f'({k}: {v})' for k, v in args.items())}")

        response = self.make_assistant_call(action, ai_model=ai_model)
        return response.message

    @keyword
    def delete_assistant_by_id(self, ai_model: str = None, id: str = None):
        """
        Deletes the assistant with the specified Id

        If that assistant is also the active assistant, there will be no active assistant.
        Either create a new assistant or set a new assistant as active.

        The following arguments can be used (arguments with a * are required):
        - *ai_model: str: The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
        - *id: str: The Id of the assistant. This an Id created by the AI model itself. e.g. "asst_0Ta3aCdE675foHxkLTnujjgl"
        """
        action = "delete_assistant_by_id"
        # If arguments are not given directly, get their default value. This is the value of the class attribute with the same name
        ai_model, id = self.get_default_values_for_arguments(ai_model=ai_model, id=id)
        # Log the arguments
        args = locals()
        args.pop("self")
        logger.debug(f"Calling keyword `Delete Assistant By Id` with arguments: {', '.join(f'({k}: {v})' for k, v in args.items())}")
        # Validate arguments
        self.validate_input_arguments(id=id)

        response = self.make_assistant_call(action, ai_model=ai_model, id=id)
        return response.message

    @keyword
    def attach_files(self, ai_model: str = None, file_paths: list[str] = None):
        """
        Attaches files to the active assistant

        These files can be used by the assistant in any thread as opposed to sending files with a prompt.

        The following arguments can be used (arguments with a * are required):
        - *ai_model: str: The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
        - file_paths: str: A list of paths that determine which files get send with the prompt.
            Both paths to files and paths to folder can be used. Paths to files will directly add that file to the prompt.
            Paths to folders will look into all files in that folder and add them to the prompt.
            e.g. ["src/main.py", "src/resources"]
        """
        action = "attach_files"
        # If arguments are not given directly, get their default value. This is the value of the class attribute with the same name
        ai_model, = self.get_default_values_for_arguments(ai_model=ai_model)
        # Log the arguments
        args = locals()
        args.pop("self")
        logger.debug(f"Calling keyword `Attach Files` with arguments: {', '.join(f'({k}: {v})' for k, v in args.items())}")
        # Validate arguments
        self.validate_input_arguments(file_paths=file_paths)

        response = self.make_assistant_call(action, ai_model=ai_model, file_paths=file_paths)
        return response.message

    @keyword
    def get_active_assistant_id(self, ai_model: str = None):
        """
        Returns the Id of the active assistant

        The following arguments can be used (arguments with a * are required):
        - *ai_model: str: The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
        """
        action = "get_active_assistant_id"
        # If arguments are not given directly, get their default value. This is the value of the class attribute with the same name
        ai_model, = self.get_default_values_for_arguments(ai_model=ai_model)
        # Log the arguments
        args = locals()
        args.pop("self")
        logger.debug(f"Calling keyword `Get Active Assistant Id` with arguments: {', '.join(f'({k}: {v})' for k, v in args.items())}")
        # If arguments are not given directly, get their default value. This is the value of the class attribute with the same name
        response = self.make_assistant_call(action, ai_model=ai_model)
        return response.message

    @keyword
    def create_new_thread(self, ai_model: str = None):
        """
        Create a new thread

        Creating a new thread effectively restarts the conversation.

        The following arguments can be used (arguments with a * are required):
        - *ai_model: str: The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
        """
        action = "create_new_thread"
        # If arguments are not given directly, get their default value. This is the value of the class attribute with the same name
        ai_model, = self.get_default_values_for_arguments(ai_model=ai_model)
        # Log the arguments
        args = locals()
        args.pop("self")
        logger.debug(f"Calling keyword `Create New Thread` with arguments: {', '.join(f'({k}: {v})' for k, v in args.items())}")
        # If arguments are not given directly, get their default value. This is the value of the class attribute with the same name
        response = self.make_assistant_call(action, ai_model=ai_model)
        return response.message

    @keyword
    def set_active_assistant(self, ai_model: str = None, id: str = None):
        """
        Sets the assistant with the specified Id as active

        This will also create a new thread

        The following arguments can be used (arguments with a * are required):
        - *ai_model: str: The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
        - *id: str: The Id of the assistant. This an Id created by the AI model itself. e.g. "asst_0Ta3aCdE675foHxkLTnujjgl"
        """
        action = "set_active_assistant"
        # If arguments are not given directly, get their default value. This is the value of the class attribute with the same name
        ai_model, id = self.get_default_values_for_arguments(ai_model=ai_model, id=id)
        # Log the arguments
        args = locals()
        args.pop("self")
        logger.debug(f"Calling keyword `Set Active Assistant` with arguments: {', '.join(f'({k}: {v})' for k, v in args.items())}")
        # If arguments are not given directly, get their default value. This is the value of the class attribute with the same name
        response = self.make_assistant_call(action, ai_model=ai_model, id=id)
        return response.message

    @keyword
    def update_assistant(
            self,
            ai_model: str = None,
            name: str = None,
            instructions: str = None,
            model: str = None,
            temperature: float = None,
            top_p: float = None,
            response_format: dict = None
    ):
        """
        Updates the parameters of the active assistant

        Accepts the same arguments as the Create Assistant keyword
        
        The following arguments can be used (arguments with a * are required):
        - *ai_model: str: The AI model to be used, e.g. "openai", "gemini", "copilot", etc. Currently supporting: "openai"
        - *name: str: The name of the assistant. This name will show up in responses and in the logs, e.g. "Bob". Max 256 characters
        - *instructions: str: The instructions given to the assistant. Here you can explain how the assistant should behave,
            e.g. "You are a software engineer that can debug my code and explain it in a easy to understand manner". Max 256,000 characters
        - model: str: AI model specfic. The model of the AI model to be used. E.g. "gpt-3.5-turbo" when using the "openai" AI model.
            Default per AI model:
                - "openai" = "gpt-3.5-turbo"
        - temperature: float: This value determines the creativity of the AI model. Can be anything from 0-2. Default = 1
        - top_p: float: Similar to temperature. Determines the selection of tokens before selecting one.
            The higher the value the more less likely tokens get added to the selection. Can be anything from 0-2. At 1,
            only the top 50% of tokens will be used when selecting a token at 0 all tokens will be taken into consideration. Default = 1
        - response_format: dict: Can be used to make the response compile to JSON.
            Set this to { "type": "json_object" } to make the response compile to JSON or None if it shouldn't necessarily.
            Default = { "type": "json_object" }
        """
        action = "update_assistant"
        # If arguments are not given directly, get their default value. This is the value of the class attribute with the same name
        ai_model, name, instructions, model, temperature, top_p, response_format = self.get_default_values_for_arguments(
            ai_model=ai_model,
            name=name,
            instructions=instructions,
            model=model,
            temperature=temperature,
            top_p=top_p,
            response_format=response_format
        )
        # Log the arguments
        args = locals()
        args.pop("self")
        logger.debug(f"Calling keyword `Update Assistant` with arguments: {', '.join(f'({k}: {v})' for k, v in args.items())}")
        # Validate arguments
        self.validate_input_arguments(name=name, instructions=instructions, temperature=temperature, top_p=top_p)
        response = self.make_assistant_call(action, ai_model=ai_model, name=name, instructions=instructions, model=model, temperature=temperature, top_p=top_p, response_format=response_format)
        return response.message


    # Validation methods
    def is_valid_name(self, name: str):
        if name is None:
            error_message = f"Argument `name` can not be None. Either set it using the `Set Name` keyword or supply the argument directly."
            logger.error(error_message)
            raise ValueError(error_message)

    def is_valid_instructions(self, instructions: str):
        if instructions is None:
            error_message = f"Argument `instructions` can not be None. Either set it using the `Set Instructions` keyword or supply the argument directly."
            logger.error(error_message)
            raise ValueError(error_message)

    def is_valid_id(self, id: str):
        if id is None:
            error_message = f"Argument `id` can not be None. Either set it using the `Set Id` keyword or supply the argument directly."
            logger.error(error_message)
            raise ValueError(error_message)

    def is_valid_file_paths(self, file_paths: str):
        if file_paths is None or not file_paths:
            error_message = f"Invalid value `{file_paths}`. Argument `file_paths` can not be None nor an empty list. Argument `file_paths` can not be set, to use keyword, supply the argument `file_paths` directly."
            logger.error(error_message)
            raise ValueError(error_message)


    # Setters
    @keyword
    def set_id(self, id: str = None):
        """
        Setter for the ID argument.
        id: str: The ID to be assigned.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set ID. Changing ID from `{self.id}` to `{id}`")
        self.id = id

    @keyword
    def set_name(self, name: str = None):
        """
        Setter for the Name argument.
        name: str: The name to be assigned.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Name. Changing Name from `{self.name}` to `{name}`")
        self.name = name

    @keyword
    def set_instructions(self, instructions: str = None):
        """
        Setter for the Instructions argument.
        instructions: str: The instructions to be assigned.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Instructions. Changing Instructions from `{self.instructions}` to `{instructions}`")
        self.instructions = instructions
