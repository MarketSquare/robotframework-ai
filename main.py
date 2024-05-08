import pytest
from robot import run

from modules.chatbot.Chatbot import Chatbot
from modules.real_test_data_generator.RealTestDataGenerator import RealTestDataGenerator as RTDG

def real_test_data_generator():
    generator = RTDG()
    response = generator.generate_test_data("openai", "address", amount=3, country="czech republic")
    print("\n\n\n", response, "\n\n\n")

def chatbot():
    message = "If I say water you say fire"
    generator = Chatbot()
    response = generator.generate_response("openai", message)
    print("\n\n\n", response, "\n\n\n")
    message = "Water"
    response = generator.generate_response("openai", message, keep_history=True)
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
