from RobotFrameworkAI.ai_interface.ai_model_tools.BaseAITool import BaseAITool


class TextGeneratorTool(BaseAITool):
    def __init__(self) -> None:
        super().__init__()
        self.tool_name = "text_generation"

    def call_ai_tool(self, prompt):
        pass