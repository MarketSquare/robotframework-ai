
class TestDataGenerator:
    """
    The interface for all TestDataGenerators

    The RealTestDataGenerator use TestDataGenerator's to generate the test data.
    Each TestDataGenerator is in charge of creating a system and a user message, this is the actual question
    sent to the ai. This will go to the AI model and eventually a Response object will be returned.
    Each TestDataGenerator should take the usefull information out of the Response and return it in a way
    that is most usefull to the user.

    As of now, the only TestDataGenerator is the AddressGenerator, this can be expanded on.
    There is also a UserDataGenerator although that is for now just an example of an implementation.

    To create new types of test data generators, create a new class in the test_data_generators folder.
    Have that class inherit the TestDataGenerator interface and implement the methods: create_prompt_message
    and format_response. The create_prompt_message method should create a system message and a user message,
    supply those to the create_message method and return its result. The format_response takes the Response,
    extract the message from the AI model and format it in a way that is most usefull to the user.

    Adding an object of this class to the generators in the RealTestDataGenerator class will allow you to
    to use that test data generator for the generation of data.
    """
    def __init__(self) -> None:
        self.type = "base_test_data_generator"

    def create_prompt_messages(self, amount, format):
        pass

    def format_response(self, response):
        pass
