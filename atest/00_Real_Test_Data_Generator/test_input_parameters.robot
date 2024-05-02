*** Settings ***
Library    ../../ai_interface/modules/real_test_data_generator/RealTestDataGenerator.py

*** Test Cases ***
Test Invalid AI Model
    [Documentation]    Test when AI Model is invalid
    Setup Test Parameters
    Set AI Model    invalid_model
    ${error_message} =    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Parameters

Test Invalid Type
    [Documentation]    Test when Type is invalid
    Setup Test Parameters
    Set Type    invalid_type
    ${error_message} =    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Parameters

Test Invalid Max Tokens
    [Documentation]    Test when Max Tokens is invalid
    Setup Test Parameters    # Set valid parameters first
    Set Max Tokens    5000    # Set invalid Max Tokens value
    ${error_message} =    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Parameters

Test Invalid Model
    [Documentation]    Test when Model is invalid
    Setup Test Parameters    # Set valid parameters first
    Set Model    invalid_model    # Set invalid Model value
    ${error_message} =    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Parameters

Test Invalid Temperature
    [Documentation]    Test when Temperature is invalid
    Setup Test Parameters    # Set valid parameters first
    Set Temperature    -1.5    # Set invalid Temperature value
    ${error_message} =    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Parameters

Test Invalid Top P
    [Documentation]    Test when Top P is invalid
    Setup Test Parameters    # Set valid parameters first
    Set Top P    2.5    # Set invalid Top P value
    ${error_message} =    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Parameters

Test Invalid Frequency Penalty
    [Documentation]    Test when Frequency Penalty is invalid
    Setup Test Parameters    # Set valid parameters first
    Set Frequency Penalty    -3.0    # Set invalid Frequency Penalty value
    ${error_message} =    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Parameters

Test Invalid Presence Penalty
    [Documentation]    Test when Presence Penalty is invalid
    Setup Test Parameters    # Set valid parameters first
    Set Presence Penalty    3.0    # Set invalid Presence Penalty value
    ${error_message} =    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Parameters

Test All Valid
    [Documentation]    Test when all parameters are valid
    Setup Test Parameters
    Generate Test Data With Parameters

Test Multiple Invalid
    [Documentation]    Test when multiple parameters are invalid
    Setup Test Parameters
    Set AI Model    invalid_ai_model
    Set Type    invalid_type
    Set Max Tokens    5000
    Set Model    invalid_model
    Set Temperature    3
    Set Top P    3
    Set Frequency Penalty    3
    Set Presence Penalty    3
    ${error_message} =    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Parameters


*** Keywords ***
Setup Test Parameters
    Set AI Model    openai
    Set Type    address
    Set Amount   3
    Set Format    "{'addresses':[{'address': address}]}"
    Set Max Tokens    256
    Set Model    gpt-3.5-turbo
    Set Temperature    1
    Set Top P    1
    Set Frequency Penalty    0
    Set Presence Penalty    0
    Set Country    Czech Republic

Generate Test Data With Parameters
    [Documentation]    Generates test data using the specified parameters.
    ${test_data} =    Generate Test Data
    ...    ${AI_MODEL}
    ...    ${TYPE}
    ...    ${AMOUNT}
    ...    ${FORMAT}
    ...    ${MAX_TOKENS}
    ...    ${MODEL}
    ...    ${TEMPERATURE}
    ...    ${TOP_P}
    ...    ${FREQUENCY_PENALTY}
    ...    ${PRESENCE_PENALTY}
    ...    country=${COUNTRY}
    RETURN    ${test_data}

Set AI Model
    [Arguments]    ${ai_model}
    Set Test Variable    ${AI_MODEL}    ${ai_model}
Set Type
    [Arguments]    ${type}
    Set Test Variable    ${TYPE}    ${type}
Set Amount
    [Arguments]    ${amount}
    Set Test Variable    ${AMOUNT}    ${amount}
Set Country
    [Arguments]    ${country}
    Set Test Variable    ${COUNTRY}    ${country}
Set Format
    [Arguments]    ${format}
    Set Test Variable    ${FORMAT}    ${format}
Set Model
    [Arguments]    ${model}
    Set Test Variable    ${MODEL}    ${model}
Set Temperature
    [Arguments]    ${temperature}
    Set Test Variable    ${TEMPERATURE}    ${temperature}
Set Max Tokens
    [Arguments]    ${max_tokens}
    Set Test Variable    ${MAX_TOKENS}    ${max_tokens}
Set Top P
    [Arguments]    ${top_p}
    Set Test Variable    ${TOP_P}    ${top_p}
Set Frequency Penalty
    [Arguments]    ${frequency_penalty}
    Set Test Variable    ${FREQUENCY_PENALTY}    ${frequency_penalty}
Set Presence Penalty
    [Arguments]    ${presence_penalty}
    Set Test Variable    ${PRESENCE_PENALTY}    ${presence_penalty}
   

