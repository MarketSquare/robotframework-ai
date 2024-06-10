import logging
import os
from RobotFrameworkAI.ai_interface.ai_model_tools.BaseAITool import BaseAITool


logger = logging.getLogger(__name__)


class AssistantTool(BaseAITool):

    # File types that can be used with the assistant
    ALLOWED_EXTENSIONS = {"c", "cpp", "css", "csv", "docx", "gif", "html", "java", "jpeg", "jpg", "js", "json", "md", "pdf", 
                        "php", "png", "pptx", "py", "rb", "tar", "tex", "ts", "txt", "webp", "xlsx", "xml", "zip"}
    
    
    def __init__(self) -> None:
        print(__name__)
        super().__init__()
        self.tool_name = "assistant"

    def call_ai_tool(self, prompt):
        assistant_data = prompt.ai_tool_data
        logger.debug(f"Calling the `{prompt.config.ai_model}` assistant with action {assistant_data.action}, {prompt}")
        match assistant_data.action:
            case "send_prompt":
                return self.send_prompt_to_assistant(prompt)
            case "get_active_assistant_id":
                return self.get_active_assistant_id()
            case "create_assistant":
                return self.create_assistant(prompt)
            case "delete_assistant":
                return self.delete_assistant(assistant_data.id)
            case "attach_files":
                files = self.prepare_files(assistant_data.file_paths)
                logger.debug(f"From the file/folder paths `{assistant_data.file_paths}`, the following files get added: `{"`, `".join([file[0] for file in files])}`")
                return self.attach_files_to_assistant(files)
            case _:
                error_message = f"Invalid value `{assistant_data.action}` for assistant data action"
                logger.error(error_message)
                raise ValueError(error_message)
                

    # def setup_assistant(self, prompt):
    #     assistant_data = prompt.ai_tool_data
    #     file_paths = self.collect_files(assistant_data.folder_path)
    #     # Add the file paths to the instructions as this could aid the assistant in understanding the files
    #     assistant_data.instructions += f"\n The files structure of the given files is as follows:\n{"\n".join(file_paths)}"
    #     self.assistant = self.create_assistant(prompt, file_paths)
    #     # self.attach_files_to_assistant(file_paths)

    def prepare_files(self, files):
        file_paths = set()
        for item in files:
            # Check whether item is a file- or a folder path
            if '.' in item:
                file_paths.add(item)
            else:
                file_paths.update(self.collect_files_from_folder(item))
        return [(path, self.read_file_with_placeholder_content_if_empty(path)) for path in file_paths]

    def collect_files_from_folder(self, folder_path):
        file_paths = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if self.has_allowed_extension(file):
                    full_path = os.path.join(root, file)
                    file_paths.append(full_path)
        logger.debug(f"Found the following files in `{folder_path}`: `{"`, `".join(file_paths)}`")
        return file_paths

    @staticmethod
    def has_allowed_extension(file_name):
        """
        Check if the file has one of the allowed extensions.

        Parameters:
        - file_name (str): The name of the file.

        Returns:
        - bool: True if the file has an allowed extension, False otherwise.
        """
        return file_name.split('.')[-1] in AssistantTool.ALLOWED_EXTENSIONS

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

    def create_assistant(self, prompt):
        pass

    def delete_assistant(self, id):
        pass

    def delete_active_assistant(self):
        pass

    def list_assistant(self):
        pass

    def get_assistant(self, id):
        pass

    def get_assistant_by_name(self, name):
        """
        Attempts to get the assistant by name.

        Names aren't neccesarilly unique, 
        """
        pass

    def attach_files_to_assistant(self, file_paths):
        pass

    def send_prompt_to_assistant(self, prompt):
        pass

    def get_active_assistant_id(self):
        pass
