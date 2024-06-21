*** Settings ***
Documentation    Tests the keep history flag for the keyword generate response
Library    ../../src/RobotFrameworkAI/modules/chatbot/Chatbot.py
Test Setup    Setup Test Arguments


*** Test Cases ***
Test Keep History
    [Documentation]    Tests whether the AI remembers to respond with fire after saying water
    Set System Message    You are helpful
    Set Message    If i say water you say fire
    Generate Response
    Set Message    Water
    Set Keep History    True
    ${response}    Generate Response
    Should Contain    ${response}    fire    ignore_case=True
    Set Keep History    False
    ${response}    Generate Response
    Should Not Contain    ${response}    fire    ignore_case=True


*** Keywords ***
Setup Test Arguments
    [Documentation]    Set default test arguments
    Set AI Model    openai
    Set Model    gpt-3.5-turbo
    Set Max Tokens    256
    Set Temperature    1
    Set Top P    .5
    Set Frequency Penalty    0
    Set Presence Penalty    0
    Set Keep History    False
