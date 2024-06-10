from RobotFrameworkAI.objects.prompt.ai_tool_data.AIToolData import AIToolData


class AssistantData(AIToolData):
    """
    Additional data used when using an AI assistant tool.

    action: determines what you want to do with the AI assistant.
        Valid actions are:
    file_paths: a list of paths to files/folders to attach to the assistant.
        When provding folders, all files in the folder get added.
    """
    def __init__(self, action, id = None, name = None, instructions = "", file_paths = None) -> None:
        super().__init__()
        self.action = action
        self.id = id
        self.name = name
        self.instructions = instructions
        self.file_paths = file_paths

    def __str__(self):
        return (
            f"(Action: {self.action})"
            + (f", (ID: {self.id})" if self.id is not None else "")
            + (f", (Name: {self.name})" if self.name is not None else "")
            + (f", (Instructions: {self.instructions})" if self.instructions else "")
            + (f", (Folder Paths: {self.file_paths})" if self.file_paths else "")
        )