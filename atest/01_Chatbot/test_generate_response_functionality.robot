*** Settings ***
Documentation    Tests the keep history flag for the keyword generate response
Library    ../../src/RobotFrameworkAI/modules/chatbot/Chatbot.py


*** Variables ***
${AI_MODEL}    value
${MODEL}    value
${MESSAGE}    value
${MAX_TOKENS}    value
${TEMPERATURE}    value
${TOP_P}    value
${FREQUENCY_PENALTY}    value
${PRESENCE_PENALTY}    value
${KEEP_HISTORY}    value


*** Test Cases ***
Test Keep History
    [Documentation]    Tests whether the AI remembers to respond with fire after saying water
    Setup Test Arguments
    Set Message    If i say water you say fire
    Generate Response With Arguments
    Set Message    Water
    Set Temperature    0
    Set Top P    0
    Set Keep History    True
    ${response}    Generate Response With Arguments
    Should Contain    ${response}    fire    ignore_case=True


*** Keywords ***
Setup Test Arguments
    [Documentation]    Set default test arguments
    Set AI Model    openai
    Set Model    gpt-3.5-turbo
    Set Max Tokens    256
    Set Temperature    1
    Set Top P    1
    Set Frequency Penalty    0
    Set Presence Penalty    0
    Set Keep History    False

Generate Response With Arguments
    [Documentation]    Generates a response to a prompt
    ${response}    Generate Response
    ...    ${AI_MODEL}
    ...    ${MESSAGE}
    ...    ${MODEL}
    ...    ${MAX_TOKENS}
    ...    ${TEMPERATURE}
    ...    ${TOP_P}
    ...    ${FREQUENCY_PENALTY}
    ...    ${PRESENCE_PENALTY}
    ...    ${KEEP_HISTORY}
    RETURN    ${response}

Set AI Model
    [Documentation]    Set AI model for response generation
    [Arguments]    ${AI_MODEL}
    VAR    ${AI_MODEL}    ${AI_MODEL}    scope=test

Set Message
    [Documentation]    Set the message for response generation
    [Arguments]    ${MESSAGE}
    VAR    ${MESSAGE}    ${MESSAGE}    scope=test

Set Model
    [Documentation]    Set the model for response generation
    [Arguments]    ${MODEL}
    VAR    ${MODEL}    ${MODEL}    scope=test

Set Max Tokens
    [Documentation]    Set the maximum number of tokens for response generation
    [Arguments]    ${MAX_TOKENS}
    VAR    ${MAX_TOKENS}    ${MAX_TOKENS}    scope=test

Set Temperature
    [Documentation]    Set the temperature for response generation
    [Arguments]    ${TEMPERATURE}
    VAR    ${TEMPERATURE}    ${TEMPERATURE}    scope=test

Set Top P
    [Documentation]    Set the top P value for response generation
    [Arguments]    ${TOP_P}
    VAR    ${TOP_P}    ${TOP_P}    scope=test

Set Frequency Penalty
    [Documentation]    Set the frequency penalty for response generation
    [Arguments]    ${FREQUENCY_PENALTY}
    VAR    ${FREQUENCY_PENALTY}    ${FREQUENCY_PENALTY}    scope=test

Set Presence Penalty
    [Documentation]    Set the presence penalty for response generation
    [Arguments]    ${PRESENCE_PENALTY}
    VAR    ${PRESENCE_PENALTY}    ${PRESENCE_PENALTY}    scope=test

Set Keep History
    [Documentation]    Set the keep history boolean for response generation
    [Arguments]    ${KEEP_HISTORY}
    VAR    ${KEEP_HISTORY}    ${KEEP_HISTORY}    scope=test
