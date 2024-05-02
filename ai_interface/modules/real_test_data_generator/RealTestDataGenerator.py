from robot.api.deco import keyword, library

from ai_interface.modules.Module import Module
from ai_interface.modules.real_test_data_generator.test_data_generators.AddressGenerator import AddressGenerator
from ai_interface.modules.real_test_data_generator.test_data_generators.UserDataGenerator import UserDataGenerator


@library
class RealTestDataGenerator(Module):    
    # Robot library stuff
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_VERSION = "1"

    def __init__(self) -> None:
        super().__init__("real_test_data_generator")
        self.generators = {
            "address": AddressGenerator(),
            "user_data": UserDataGenerator(),
        }
    
    @keyword
    def generate_test_data(
            self,
            ai_model:str,
            type:str,
            amount:int=3,
            format:str=None,
            max_tokens:int=256,
            model:str="gpt-3.5-turbo",
            temperature:float=1,
            top_p:float=1,
            frequency_penalty:float=0,
            presence_penalty:float=0,
            **kwargs
        ):
        self.validate_input(type, max_tokens, temperature, top_p, frequency_penalty, presence_penalty)
        generator = self.generators[type]
        message = generator.create_prompt(amount, format, kwargs)
        response = self.ai_interface.send_prompt(
            self.name, ai_model, message, max_tokens, model, temperature, top_p, frequency_penalty, presence_penalty
        )
        response = generator.format_response(response)
        return response

    def validate_input(self, type:str, max_tokens:int, temperature:float, top_p:float, frequency_penalty:float, presence_penalty:float):
        error_messages = []
        if not type in self.generators:
            error_messages.append(f"Invalid value '{type}' for 'type'. Value must be in: {', '.join(self.generators.keys())}.")
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
    