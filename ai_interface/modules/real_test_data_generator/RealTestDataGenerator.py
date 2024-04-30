import json
from robot.api.deco import keyword, library

from ai_interface.modules.Module import Module


@library
class RealTestDataGenerator(Module):
    def __init__(self) -> None:
        super().__init__("real_test_data_generator")
    
    @keyword
    def generate_test_addresses(
            self,
            ai_model:str,
            count:int=3,
            country:str=None,
            format:str=None,
            max_tokens:int=256,
            model:str="gpt-3.5-turbo",
            temperature:float=1,
            top_p:float=1,
            frequency_penalty:float=0,
            presence_penalty:float=0
        ):
        self.validate_input(max_tokens, temperature, top_p, frequency_penalty, presence_penalty)
        message = self.create_prompt(count, format, country)
        response = self.ai_interface.send_prompt(
            self.name, ai_model, message, max_tokens, model, temperature, top_p, frequency_penalty, presence_penalty
        )
        response = self.format_response(response)
        return response

    def create_prompt(self, count=3, format=None, country=None):
        system_message = f"""
            You generate a list of just addresses nothing else not the company name in json.
            Call the list 'addresses' and the addresses 'address', don't use any newline characters
        """
        system_message += f", in the format: {format}" if format is not None else ""
        country_message = country if country is not None else "different countries around the world"
        user_message = f"Give me a list {count} different companies from {country_message} and the address of their HQ"
        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    
    def format_response(self, response:object):
        response = response.choices[0].message.content
        addresses = json.loads(response)
        return [address["address"] for address in addresses["addresses"]]
    
    def validate_input(self, max_tokens, temperature, top_p, frequency_penalty, presence_penalty):
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
        return error_messages
    
    def is_valid_max_tokens(self, max_tokens):
        return 0 < max_tokens <= 4096
    def is_valid_temperature(self, temperature):
        return 0 <= temperature <= 2
    def is_valid_top_p(self, top_p):
        return 0 <= top_p <= 2
    def is_valid_frequency_penalty(self, frequency_penalty):
        return -2 <= frequency_penalty <= 2
    def is_valid_presence_penalty(self, presence_penalty):
        return -2 <= presence_penalty <= 2
    