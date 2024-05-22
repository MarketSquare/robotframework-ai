import pytest
from robot import run

from RobotFrameworkAI.modules.chatbot.Chatbot import Chatbot
from RobotFrameworkAI.modules.real_test_data_generator.RealTestDataGenerator import RealTestDataGenerator as RTDG

def real_test_data_generator():
    generator = RTDG()
    generator.set_ai_model("openai")
    generator.set_type("address")
    generator.set_amount(3)
    generator.set_kwarg("country", "czech republic")
    response = generator.generate_test_data()
    print("\n\n\n", response, "\n\n\n")

def chatbot():
    message = "If I say water you say fire"
    generator = Chatbot()
    generator.set_ai_model("openai")
    generator.set_message(message)
    response = generator.generate_response()
    print("\n\n\n", response, "\n\n\n")
    message = "Water"
    generator.set_message(message)
    generator.set_keep_history(True)
    response = generator.generate_response()
    print("\n\n\n", response, "\n\n\n")


def robot_tests(s=''):
    run("atest/"+s)

def pytests():
    pytest.main(["utest/"])

if __name__ == "__main__":
    real_test_data_generator()
    chatbot()
    robot_tests()
    pytests()
