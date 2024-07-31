import json
from RobotFrameworkAI.modules.real_test_data_generator.test_data_generators.TestDataGenerator import TestDataGenerator
import logging


logger = logging.getLogger(__name__)


class AddressGenerator(TestDataGenerator):
    """
    The TestDataGenerator in charge of generating addresses.

    This TestDataGenerator creates the request for the AI model to generate address.
    It also takes the test data out of the Response and turns it to a list of addresses. 
    """
    def __init__(self) -> None:
        super().__init__()
        self.type = "address"

    def create_prompt_messages(self, amount:int, format:str, address_kwargs:dict):
        system_message = """
            You generate a list of just addresses nothing else not the company name, in json.
            Call the list 'addresses' and each list item is a dictionary with the key 'address', don't use any newline characters
        """
        country = address_kwargs.get("country", None)
        system_message += f", in the format: {format}" if format is not None else ""
        country_message = country if country is not None else "different countries around the world"
        user_message = f"Give me a list {amount} different companies from {country_message} and the address of their HQ"
        return system_message, user_message

    def format_response(self, response):
        response = response.message
        try:
            addresses = json.loads(response)
        except json.JSONDecodeError as e:
            error = f"The response couldn't be parsed to JSON. Response: {response}. Error {e}"
            logger.error(error)
            raise
        return [address["address"] for address in addresses["addresses"]]