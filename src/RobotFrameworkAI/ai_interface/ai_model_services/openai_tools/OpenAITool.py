from RobotFrameworkAI.ai_interface.ai_model_services.AIModelTool import AIModelTool


class OpenAITool(AIModelTool):
    """
    The abstract class for all OpenAI tools 

    This class contains common data for all OpenAI tool.
    """
    def __init__(self) -> None:
        super().__init__()
        self.ai_model_name:str = "openai"
        self.models:list[str] = ["gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini"]
        self.default_model:str = "gpt-4o-mini"

    def format_prompt_message(self, role:str, message:str):
        """
        Formats and returns a singular message in the way the OpenAI API expects it to
        """
        return {"role": role, "content": message}

    def format_prompt_messages(self, system_message: str, user_message: str, history: list):
        """
        Formats and returns messages the way the OpenAI API expects it to

        Returns a list of singular messages which always includes a user message at the end.
        Optionally adds a system message at the front.
        If given chat history, will put the history between the system and user message.
        History is a list of user and assistant message where each assistant message is
        the response of the OpenAI API.
        """
        prompt_messages = []
        if system_message is not None:
            prompt_messages.append(self.format_prompt_message("system", system_message))
        if history:
            for entry in history:
                for role, message in entry.items():
                    prompt_messages.append(self.format_prompt_message(role, message))
        if user_message is not None:
            prompt_messages.append(self.format_prompt_message("user", user_message))
        return prompt_messages
