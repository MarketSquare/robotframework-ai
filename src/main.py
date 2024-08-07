import pytest
from robot import run

from RobotFrameworkAI.modules.chatbot.Chatbot import Chatbot
from RobotFrameworkAI.modules.real_test_data_generator.RealTestDataGenerator import RealTestDataGenerator as RTDG
from RobotFrameworkAI.modules.assistant.Assistant import Assistant

from RobotFrameworkAI.logger.logger import setup_logging

def real_test_data_generator():
    generator = RTDG()
    generator.set_ai_model("openai")
    generator.set_type("address")
    generator.set_amount(3)
    generator.set_kwarg("country", "czech republic")
    response = generator.generate_test_data()
    print("\n\n\n", response, "\n\n\n")

def chatbot():
    generator = Chatbot()
    generator.set_ai_model("openai")
    user_message = "If I say water you say fire"
    generator.set_message(user_message)
    response = generator.generate_response()
    print("\n\n\n", response, "\n\n\n")
    message = "Water"
    generator.set_message(message)
    generator.set_keep_history(True)
    response = generator.generate_response()
    print("\n\n\n", response, "\n\n\n")

def assistant():
    assistant = Assistant()
    assistant.set_name("Assistant")
    assistant.set_instructions("You are a software enigineer.")
    assistant.set_ai_model("openai")
    assistant.set_message((
        "Do you see how I can improve my code?"
    ))
    assistant.create_assistant()
    assistant.update_assistant()
    assistant.attach_files(file_paths=["src/RobotFrameworkAI"])
    print(assistant.send_message())
    assistant.delete_assistant()
def robot_tests(s=''):
    run("atest/"+s, listener="atest/listeners/LoggerListener.py")

def pytests():
    pytest.main(["utest/"])

if __name__ == "__main__":
    setup_logging(enabled=True, for_tests=False, console_logging=False, file_logging=True)
    
    real_test_data_generator()
    chatbot()
    assistant()
    robot_tests()
    pytests()
