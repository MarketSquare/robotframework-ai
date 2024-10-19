import logging
import os
from RobotFrameworkAI.ai_interface.ai_model_tools.AIToolType import AIToolType


logger = logging.getLogger(__name__)


class AssistantTool(AIToolType):
    """
    The abstract class for all assistant tools

    There are multiple ways to interact with assistants. Like creating an assistant or deleting one.
    For each of these actions an abstract methods is created.

    When recieving a Prompt, this class will call the method that is in charge of the action as per the Prompt.

    This class can also take a list of files and folders and take their context so it can be attached
    to the assistant or send with a message.

    For each abstract method, documentation is provided. This removes the need for documentation in subclasses.
    """

    # File types that can be used with the assistant
    ALLOWED_EXTENSIONS = {"c", "cpp", "css", "csv", "docx", "gif", "html", "java", "jpeg", "jpg", "js", "json", "md", "pdf", 
                        "php", "png", "pptx", "py", "rb", "tar", "tex", "ts", "txt", "webp", "xlsx", "xml", "zip"}
    
    
    def __init__(self) -> None:
        print(__name__)
        super().__init__()
        self.tool_name = "assistant"
        self.thread = None

    def call_ai_tool(self, prompt):
        """
        Calls the method that handles the handles the right action as per the Prompt

        The action attribute from the Prompt can have several different values that coincide with the name of the methods
        that handle that particular action.

        Using a dynamic approach, this method checks if there is a method in this class with the same name as the action attribute.
        If it exist call, that method and give the prompt as argument.

        Returns the a Response object created by method which corresponds to the action attribute
        """
        assistant_data = prompt.ai_tool_data
        logger.debug(f"Calling the `{prompt.config.ai_model}` assistant with action {assistant_data.action}, {prompt}")

        if hasattr(self, assistant_data.action):
            method = getattr(self, assistant_data.action)
            return method(prompt)
        else:
            error_message = f"Invalid value `{assistant_data.action}` for assistant data action"
            logger.error(error_message)
            raise ValueError(error_message)

    def prepare_files(self, files):
        f"""
        Given a list of paths to folders and files.
        Returns a list of tuples with the path to each file and its content.
        
        Paths to folders can be included. In such case all files within that folder get added aswell.

        Only files of a certain type can be used with assistants.
        These file types are: `{"`, `".join(self.ALLOWED_EXTENSIONS)}`.
        """
        file_paths = set()
        for item in files:
            # Check whether item is a file- or a folder path
            if '.' in item and self.has_allowed_extension(item):
                file_paths.add(item)
            else:
                file_paths.update(self.collect_files_from_folder(item))
        return [(path, self.read_file_with_placeholder_content_if_empty(path)) for path in file_paths]

    def collect_files_from_folder(self, folder_path):
        """
        Given a path to a folder, will look for all files within that folder and all its subfolders.
        Returns a list with the path to every file that is of a type that can be handled by assistants.
        """
        file_paths = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if self.has_allowed_extension(file):
                    full_path = os.path.join(root, file)
                    file_paths.append(full_path)
        logger.debug(f"Found the following files in `{folder_path}`: `{'`, `'.join(file_paths)}`")
        return file_paths

    @staticmethod
    def has_allowed_extension(file_path):
        """
        Check if the file has one of the allowed extensions.

        Parameters:
        - file_path (str): The name of the file.

        Returns:
        - bool: True if the file has an allowed extension, False otherwise.
        """
        return file_path.split('.')[-1] in AssistantTool.ALLOWED_EXTENSIONS

    @staticmethod
    def read_file_with_placeholder_content_if_empty(file_path):
        """
        Read a file and return its content. If the file is empty, return placeholder content.

        Parameters:
        - file_path (str): The path to the file.

        Returns:
        - str: The content of the file or placeholder content if the file is empty.
        """
        if os.path.getsize(file_path) == 0:
            return "# This is a placeholder for an empty file\n"
        with open(file_path, 'r') as file:
            return file.read()

    # Actions
    def create_assistant(self, prompt):
        """
        Creates a new assistant and returns its Id

        This new assistant will become the active assistant and a new thread will be created.
        """
        pass

    def send_message(self, prompt):
        """
        Sends a prompt to the active assistant and returns its response

        By either setting file_paths or supplying the argument in the method call, files can be send with it aswell.
        Make sure to unset file_paths to not send it with each prompt.
        """
        pass

    def delete_assistant(self, _):
        """
        Deletes the active assistant

        After deleting the active assistant, there will be no active assistant.
        Either create a new assistant or set a new assistant as active.
        """
        pass

    def delete_assistant_by_id(self, prompt):
        """
        Deletes the assistant with the specified Id

        If that assistant is also the active assistant, there will be no active assistant.
        Either create a new assistant or set a new assistant as active.
        """
        pass

    def attach_files(self, prompt):
        """
        Attaches files to the active assistant

        These files can be used by the assistant in any thread as opposed to sending files with a prompt.
        """
        pass

    def get_active_assistant_id(self, _):
        """
        Returns the Id of the active assistant
        """
        pass

    def create_new_thread(self, _):
        """
        Create a new thread

        Creating a new thread effectively restarts the conversation.
        """
        pass

    def set_active_assistant(self, prompt):
        """
        Sets the assistant with the specified Id as active

        This will also create a new thread.
    	"""
        pass

    def update_assistant(self, prompt):
        """
        Updates the parameters of the active assistant

        Accepts the same arguments as the create_assistant method.
        """
        pass

    # Helper methods
    def get_assistant(self, id):
        """
        Returns the assistant with the specified Id
        """
        pass

    def upload_file(self, file):
        """
        Uploads a file to the server of the AI model and returns it id
        """
        pass

    def add_message_to_thread(self, message, file_paths=None):
        """
        Adds a message to a thread

        Optionally adds files to that same thread.
        """
        pass
