import pytest
from robot import run

from RobotFrameworkAI.modules.chatbot.Chatbot import Chatbot
from RobotFrameworkAI.modules.real_test_data_generator.RealTestDataGenerator import RealTestDataGenerator as RTDG

from RobotFrameworkAI.logger.logger_config import setup_logging

def real_test_data_generator():
    generator = RTDG()
    generator.set_ai_model("openai")
    generator.set_type("phone_number")
    generator.set_amount(5)
    # generator.set_format("")

    # generator.set_kwarg("prefix", "00")
    # generator.set_kwarg("format", "+xxx-xxx-xxx-xxx")
    # generator.set_kwarg("country", "czechia")
    # generator.set_kwarg("mix_format", "True")

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
    run("atest/"+s, listener="atest/listeners/LoggerListener.py")

def pytests():
    pytest.main(["utest/"])

if __name__ == "__main__":
    setup_logging(enabled=True, for_tests=False, console_logging=False ,file_logging=True)
    
    # real_test_data_generator()
    # chatbot()
    # robot_tests()
    # pytests()
