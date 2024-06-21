from RobotFrameworkAI.ai_interface.ai_model_tools.AIToolType import AIToolType


class TextGeneratorTool(AIToolType):
    """
    The abstract class for all text generator tools

    Text generator tools will send a prompt to the AI model and expect a response in text.
    """
    def __init__(self) -> None:
        super().__init__()
        self.tool_name = "text_generator"

    def call_ai_tool(self, prompt):
        """
        Sends a Prompt to the AI model and creates and returns a Response
        """
        pass