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
    # assistant.set_file_paths(["src/RobotFrameworkAI"])
    assistant.set_message((
        "I have a problem in my code where if it is imported in ."
        "Keywords from this file will travel through the library eventually reaching"
        "src\RobotFrameworkAI\ai_interface\ai_model_services\openai_tools\OpenAIAssistant.py."
        "This code is for the robotframework users. Make it as detailed as needed"
    ))
    assistant.create_assistant()
    assistant.update_assistant()
    # id = assistant.get_active_assistant_id()
    # assistant.set_id(id)
    # assistant.create_assistant()
    # assistant.set_active_assistant()
    assistant.attach_files(file_paths=["src/RobotFrameworkAI"])
    print(assistant.send_message())
    # assistant.send_prompt()
    # assistant.set_file_paths()
    # assistant.create_new_thread()
    # id = assistant.get_active_assistant_id()
    # assistant.set_id(id)
    # while(True):
    #     x=input("Message to ai:\n")
    #     if x == "abc":
    #         break
    #     assistant.set_message(x)
    #     assistant.send_prompt()
    assistant.delete_assistant()
def robot_tests(s=''):
    run("atest/"+s, listener="atest/listeners/LoggerListener.py")

def pytests():
    pytest.main(["utest/"])

if __name__ == "__main__":
    setup_logging(enabled=True, for_tests=False, console_logging=False ,file_logging=True)
    
    # real_test_data_generator()
    # chatbot()
    assistant()
    # robot_tests()
    # pytests()
