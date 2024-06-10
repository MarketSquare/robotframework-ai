from RobotFrameworkAI.ai_interface.ai_model_services.AIModelSpecificAITool import AIModelSpecificAITool


class OpenAITool(AIModelSpecificAITool):
    def __init__(self) -> None:
        super().__init__()
        self.ai_model_name:str = "openai"
        self.client = None
        self.models:list[str] = ["gpt-3.5-turbo", "gpt-4o"]
        self.default_model:str = "gpt-4o"
        