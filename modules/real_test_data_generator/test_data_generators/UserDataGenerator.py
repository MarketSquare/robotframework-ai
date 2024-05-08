from modules.real_test_data_generator.test_data_generators.TestDataGenerator import TestDataGenerator


class UserDataGenerator(TestDataGenerator):
    def __init__(self) -> None:
        super().__init__()

    def create_prompt_message(self, amount, format):
        pass

    def format_response(self):
        pass