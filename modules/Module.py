from ai_interface.AI_Interface import AI_Interface
from objects.prompt.Prompt import Prompt
from objects.prompt.PromptConfig import PromptConfig
from objects.prompt.PromptMetadata import PromptMetadata


class Module:

    def __init__(self, name:str="base_module") -> None:
        self.name = name
        self.ai_interface = AI_Interface()

    def create_prompt(
            self,
            ai_model:str,
            message:list[dict],
            model:str,
            max_tokens:int,
            temperature:float,
            top_p:float,
            frequency_penalty:float,
            presence_penalty:float,
            response_format:dict
        ) -> Prompt:
        config = PromptConfig(ai_model, model, response_format)
        parameters = {
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty
        }
        metadata = PromptMetadata(self.name)
        prompt = Prompt(
            config,
            message,
            parameters,
            metadata
        )
        return prompt

    def validate_default_input_parameters(self, max_tokens:int, temperature:float, top_p:float, frequency_penalty:float, presence_penalty:float):
        error_messages = []
        if not self.is_valid_max_tokens(max_tokens):
            error_messages.append(f"Invalid value '{max_tokens}' for 'max_tokens'. Value must be greater than 0 and less than or equal to 4096.")
        if not self.is_valid_temperature(temperature):
            error_messages.append(f"Invalid value '{temperature}' for 'temperature'. Value must be between 0 and 2 (inclusive).")
        if not self.is_valid_top_p(top_p):
            error_messages.append(f"Invalid value '{top_p}' for 'top_p'. Value must be between 0 and 2 (inclusive).")
        if not self.is_valid_frequency_penalty(frequency_penalty):
            error_messages.append(f"Invalid value '{frequency_penalty}' for 'frequency_penalty'. Value must be between -2 and 2 (inclusive).")
        if not self.is_valid_presence_penalty(presence_penalty):
            error_messages.append(f"Invalid value '{presence_penalty}' for 'presence_penalty'. Value must be between -2 and 2 (inclusive).")
        if error_messages:
            raise ValueError("\n".join(error_messages))
    
    def is_valid_max_tokens(self, max_tokens:int):
        return 0 < max_tokens <= 4096
    def is_valid_temperature(self, temperature:float):
        return 0 <= temperature <= 2
    def is_valid_top_p(self, top_p:float):
        return 0 <= top_p <= 2
    def is_valid_frequency_penalty(self, frequency_penalty:float):
        return -2 <= frequency_penalty <= 2
    def is_valid_presence_penalty(self, presence_penalty:float):
        return -2 <= presence_penalty <= 2