import json
from ai_interface.modules.real_test_data_generator.test_data_generators.TestDataGenerator import TestDataGenerator


class AddressGenerator(TestDataGenerator):
    def __init__(self) -> None:
        super().__init__()

    def create_prompt(self, amount:int, format:str, address_kwargs:dict):
        system_message = f"""
            You generate a list of just addresses nothing else not the company name in json.
            Call the list 'addresses' and the addresses 'address', don't use any newline characters
        """
        country = address_kwargs.get("country", None)
        system_message += f", in the format: {format}" if format is not None else ""
        country_message = country if country is not None else "different countries around the world"
        user_message = f"Give me a list {amount} different companies from {country_message} and the address of their HQ"
        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    
    def format_response(self, response:object):
        response = response.choices[0].message.content
        addresses = json.loads(response)
        return [address["address"] for address in addresses["addresses"]]