class AIModelSpecificAITool:
    def __init__(self) -> None:
        self.ai_model_name: str = None
        self.client: object = None
        self.models: list[str] = None
        self.default_model: str = None