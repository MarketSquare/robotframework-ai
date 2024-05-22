*** Settings ***
Documentation    Tests to see if the setters work as they should
Library    ../../src/RobotFrameworkAI/modules/chatbot/Chatbot.py


*** Test Cases ***
Test Required Arguments Raises Error When Not Set
    [Documentation]    Tests whether an error gets raised when not all required arguments are given.
    ...    A required argument can be set using setter. If all required arguments are set, no error
    ...    should be raised.
    Run Keyword And Expect Error    ValueError: *    Generate Response
    Set Message    1 + 1 equals?
    Run Keyword And Expect Error    ValueError: *    Generate Response
    Set Ai Model    openai
    Generate Response

Test Given Arguments Take Priority Over Set arguments
    [Documentation]    Test that if an argument is both set beforehand using a setter and given
    ...    in the keyword itself. Then the argument given with the keyword will be used. The set
    ...    argument will stay set afterwards.
    Set Ai Model    openai
    Set Message    1 + 1 equals?
    # Message is set to 1 + 1
    ${response}    Generate Response
    Should Contain    ${response}    2
    # 2 + 2 should take priority
    ${response}    Generate Response    message= 2 + 2 equals?
    Should Contain    ${response}    4
    # 1 + 1 is still set
    ${response}    Generate Response
    Should Contain    ${response}    2
