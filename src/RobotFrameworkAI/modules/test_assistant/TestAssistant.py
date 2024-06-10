from robot.api.deco import keyword, library

from RobotFrameworkAI.modules.Module import Module
import logging

from RobotFrameworkAI.objects.prompt.ai_tool_data.AssistantData import AssistantData

# List of allowed file extensions for files that can be supplied 
ALLOWED_EXTENSIONS = {
    "c", "cpp", "css", "csv", "docx", "gif", "html", "java", "jpeg", "jpg", "js", "json", "md", "pdf", 
    "php", "png", "pptx", "py", "rb", "tar", "tex", "ts", "txt", "webp", "xlsx", "xml", "zip"
}

logger = logging.getLogger(__name__)

class TestAssistant(Module):
    def __init__(self) -> None:
        super().__init__()
        self.name = "test_assistant"
        self.ai_tool = "assistant"
        self.id = None
        self.name = None
        self.file_paths = []
        self.message = ""

    def make_assistant_call(
            self,
            action:str,
            name:str = None,
            ai_model:str = None,
            model:str = None,
            temperature:float = None,
            top_p:float = None,
            response_format:dict = None,
            id:str = None,
            message:str = None,
            file_paths:list[str] = []
        ):
        ai_model, model, temperature, top_p, response_format = self.get_default_values_for_common_arguments_for_assistants(
            ai_model, model, temperature, top_p, response_format
        )
        id, name, file_paths, message = self.get_default_values_for_test_assistant_specifc_arguments(id, name, file_paths, message)
        instructions = self.get_instructions()
        ai_tool_data = AssistantData(action, id, name, instructions, file_paths)
        prompt = self.create_prompt(self.ai_tool, ai_model, None, model, None, temperature, top_p, None, None, response_format, ai_tool_data)
        response = self.ai_interface.call_ai_tool(prompt)
        return response

    def get_default_values_for_test_assistant_specifc_arguments(self, id:str, name:str, file_paths:list[str], message:str):
        id = id if id is not None else self.id
        name = name if name is not None else self.name
        file_paths = file_paths if file_paths is not None else self.file_paths
        message = message if message is not None else self.message
        return id, name, file_paths, message

    def get_instructions(self):
        return """
            You are helpfull
        """
    
    def create_assistant(
            self,
            name: str = None,
            ai_model: str = None,
            model: str = None,
            temperature: float = None,
            top_p: float = None,
            response_format: dict = None,
        ):
        """
        Sets the action to 'create_assistant' and makes the assistant call.
        """
        action = "create_assistant"
        return self.make_assistant_call(action, name, ai_model, model, temperature, top_p, response_format)

    @keyword
    def send_prompt(self, message: str = None):
        """
        Sets the action to 'send_prompt' and makes the assistant call.
        """
        action = "send_prompt"
        return self.make_assistant_call(action, message=message)

    def delete_assistant(self, id: str = None):
        """
        Sets the action to 'delete_assistant' and makes the assistant call.
        """
        action = "delete_assistant"
        return self.make_assistant_call(action, id=id)

    def attach_files(self, file_paths: list[str] = None):
        """
        Sets the action to 'attach_files' and makes the assistant call.
        """
        action = "attach_files"
        return self.make_assistant_call(action, file_paths=file_paths)

    def get_active_assistant_id(self = None):
        """
        Sets the action to 'get_active_assistant_id' and makes the assistant call.
        """
        action = "get_active_assistant_id"
        return self.make_assistant_call(action)

    # Setters
    @keyword
    def set_id(self, id: str):
        """
        Setter for the ID argument.
        id: str: The ID to be assigned.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set ID. Changing ID from `{self.id}` to `{id}`")
        self.id = id

    @keyword
    def set_name(self, name: str):
        """
        Setter for the Name argument.
        name: str: The name to be assigned.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Name. Changing Name from `{self.name}` to `{name}`")
        self.name = name

    @keyword
    def set_file_paths(self, file_paths: list):
        """
        Setter for the Folder Paths argument.
        file_paths: list: The list of folder paths to be assigned.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Folder Paths. Changing Folder Paths from `{self.file_paths}` to `{file_paths}`")
        self.file_paths = file_paths

    @keyword
    def set_message(self, message: str):
        """
        Setter for the Message argument.
        message: str: The message to be assigned.
        See the RobotFrameworkAI docs for more information about setters.
        """
        logger.debug(f"Calling keyword: Set Message. Changing Message from `{self.message}` to `{message}`")
        self.message = message

