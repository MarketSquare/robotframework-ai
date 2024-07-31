from RobotFrameworkAI.modules.real_test_data_generator.test_data_generators.TestDataGenerator import TestDataGenerator


class UserDataGenerator(TestDataGenerator):
    """
    THIS CLASS IS JUST AN EXAMPLE FOR NOW AND SHOULD/CAN NOT BE USED AS IT DOES NOTHING

    The TestDataGenerator in charge of generating user data.
    """
    def __init__(self) -> None:
        super().__init__()
        self.type = "user_data"

    def create_prompt_messages(self, amount, format):
        pass

    def format_response(self):
        pass
