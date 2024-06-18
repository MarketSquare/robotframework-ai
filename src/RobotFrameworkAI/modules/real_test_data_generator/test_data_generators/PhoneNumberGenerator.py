# NOTES
# Add KWARGS
# When letting all countries, the output formats are different
# Add smth when the country argument is something stupid - IF clause to shut it down? or take closest country?

# IMPORTS
import json
from RobotFrameworkAI.modules.real_test_data_generator.test_data_generators.TestDataGenerator import TestDataGenerator
import logging

logger = logging.getLogger(__name__)

class PhoneNumberGenerator(TestDataGenerator):
    """
    The TestDataGenerator in charge of generating phone numbers.

    This TestDataGenerator creates the request for the AI model to generate phone number.

    It also takes the test data out of the Response and turns it to a list of addresses. 
    """
    def __init__(self) -> None:
        super().__init__()

    def create_prompt_message(self, amount:int, format:str, phone_number_kwargs:dict):
        system_message = """
        You generate list of just phone numbers, nothing else, in json
        Call the list 'phone_numbers' and each list item is a dictionary with the key 'phone_number', don't use any newline characters
        """
        country = phone_number_kwargs.get("country", None)
        country_message = country if country is not None else "different countries around the world"

        # prefix_type = phone_number_kwargs.get("prefix", None)
        # prefix_type_message = prefix_type if prefix_type is not None else "international: +xxx"

        system_message += f", phone number format is {format}" if format is not None else ""
        user_message = f"Give me a list of {amount} different phone numbers from {country_message} in the same format."
        
        # Use the same format for all phone numbers regarding numbers, all the special signs (such as '-') and the spaces.
        return self.create_message(system_message, user_message)

    def format_response(self, response):
        response = response.message
        try:
            phone_numbers = json.loads(response)
        except json.JSONDecodeError as e:
            error = f"The response couldn't be parsed to JSON. Response: {response}. Error {e}"
            logger.error(error)
            raise
        return [phone_number["phone_number"] for phone_number in phone_numbers["phone_numbers"]]