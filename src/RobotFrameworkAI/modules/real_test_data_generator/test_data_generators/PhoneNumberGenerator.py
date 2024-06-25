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
        Call the list 'phone_numbers' and each list item is a dictionary with the key 'phone_number', don't use any newline characters, don't create all numbers 1 to 9 instead randomize the sequence of numbers
        """
        # Get kwargs
        prefix = phone_number_kwargs.get("prefix") if phone_number_kwargs.get("prefix") is not None else "+xxx"
        phone_format = phone_number_kwargs.get("phone_format", None)
        country = phone_number_kwargs.get("country", None)
        mix_format = True if phone_number_kwargs.get("mix_format") == True else False
        if mix_format is True: phone_format, prefix = None, "[use various different prefix types like +xxx, 00xxx and other, mix the prefixes randomly not periodically]"

        #Use prefix or override with whole format
        if phone_format is None:
            system_message += f", phone number format is not defined fully, but use this prefix/prefix definition: {prefix} and the typical format for the country specified if the country is specified."
        else:
            system_message += f", phone number format is exactly defined as: {phone_format}, ignore prefix instruction a do not output in other phone number format then specified phone number format"

        # Country and Mixer
        if country is not None and mix_format is False:
            user_message = f"Give me a list of {amount} different real phone numbers from {country} all in the absolutely same format regarding prefix, '-' signs and spaces between numbers.In any circumstances do not mix formats.."
        elif country is None and mix_format is False:
            user_message = f"Give me a list of {amount} different real phone numbers from different countries in the world, all in the absolutely same format, without dashes or spaces, regarding prefix, '-' signs and spaces between numbers.In any circumstances do not mix formats."
        elif country is not None and mix_format is True:
            user_message = f"Give me a list of {amount} different real phone numbers from {country} in different but valid formats used in real world, always include all possible real phone number formats, ignore prefix and phone number format defined earlier, randomize numbers and do not make all of them 123456789."
        else: # Country is None and mix_format is True
            user_message = f"Give me a list of {amount} different real phone numbers from different countries in the world in different but valid formats used in real world, always include all possible real phone number formats, ignore prefix and phone number format defined earlier, randomize numbers and do not make all of them 123456789.."

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