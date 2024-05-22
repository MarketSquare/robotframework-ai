*** Settings ***
Documentation    Tests the input validation for the keyword generate test data
Library    ../../src/RobotFrameworkAI/modules/real_test_data_generator/RealTestDataGenerator.py


*** Variables ***
${AI_MODEL}    value
${TYPE}    value
${MODEL}    value
${AMOUNT}    value
${FORMAT}    value
${MAX_TOKENS}    value
${TEMPERATURE}    value
${TOP_P}    value
${FREQUENCY_PENALTY}    value
${PRESENCE_PENALTY}    value
${COUNTRY}    value


*** Test Cases ***
Test Invalid AI Model
    [Documentation]    Test when AI Model is invalid
    Setup Test Arguments
    Set AI Model    invalid_model
    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Arguments

Test Invalid Type
    [Documentation]    Test when Type is invalid
    Setup Test Arguments
    Set Type    invalid_type
    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Arguments

Test Invalid Model
    [Documentation]    Test when Model is invalid
    Setup Test Arguments    # Set valid arguments first
    Set Model    invalid_model    # Set invalid Model value
    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Arguments

Test Invalid Max Tokens
    [Documentation]    Test when Max Tokens is invalid
    Setup Test Arguments    # Set valid arguments first
    Set Max Tokens    5000    # Set invalid Max Tokens value
    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Arguments

Test Invalid Temperature
    [Documentation]    Test when Temperature is invalid
    Setup Test Arguments    # Set valid arguments first
    Set Temperature    -1.5    # Set invalid Temperature value
    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Arguments

Test Invalid Top P
    [Documentation]    Test when Top P is invalid
    Setup Test Arguments    # Set valid arguments first
    Set Top P    2.5    # Set invalid Top P value
    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Arguments

Test Invalid Frequency Penalty
    [Documentation]    Test when Frequency Penalty is invalid
    Setup Test Arguments    # Set valid arguments first
    Set Frequency Penalty    -3.0    # Set invalid Frequency Penalty value
    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Arguments

Test Invalid Presence Penalty
    [Documentation]    Test when Presence Penalty is invalid
    Setup Test Arguments    # Set valid arguments first
    Set Presence Penalty    3.0    # Set invalid Presence Penalty value
    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Arguments

Test All Valid
    [Documentation]    Test when all arguments are valid
    Setup Test Arguments
    Generate Test Data With Arguments

Test Multiple Invalid
    [Documentation]    Test when multiple arguments are invalid
    Setup Test Arguments
    Set AI Model    invalid_ai_model
    Set Type    invalid_type
    Set Model    invalid_model
    Set Max Tokens    5000
    Set Temperature    3
    Set Top P    3
    Set Frequency Penalty    3
    Set Presence Penalty    3
    Run Keyword And Expect Error    ValueError: *    Generate Test Data With Arguments


*** Keywords ***
Setup Test Arguments
    [Documentation]    Set default test arguments
    Set AI Model    openai
    Set Type    address
    Set Model    gpt-3.5-turbo
    Set Amount   3
    Set Format    "{'addresses':[{'address': address}]}"
    Set Max Tokens    256
    Set Temperature    1
    Set Top P    1
    Set Frequency Penalty    0
    Set Presence Penalty    0
    Set Country    Czech Republic

Generate Test Data With Arguments
    [Documentation]    Generates test data using the specified arguments
    ${test_data} =    Generate Test Data
    ...    ${AI_MODEL}
    ...    ${TYPE}
    ...    ${MODEL}
    ...    ${AMOUNT}
    ...    ${FORMAT}
    ...    ${MAX_TOKENS}
    ...    ${TEMPERATURE}
    ...    ${TOP_P}
    ...    ${FREQUENCY_PENALTY}
    ...    ${PRESENCE_PENALTY}
    ...    country=${COUNTRY}
    RETURN    ${test_data}

Set AI Model
    [Documentation]    Set AI model for test data generation
    [Arguments]    ${AI_MODEL}
    VAR    ${AI_MODEL}    ${AI_MODEL}    scope=test

Set Type
    [Documentation]    Set the type for test data generation
    [Arguments]    ${TYPE}
    VAR    ${TYPE}    ${TYPE}    scope=test

Set Model
    [Documentation]    Set the model for test data generation
    [Arguments]    ${MODEL}
    VAR    ${MODEL}    ${MODEL}    scope=test

Set Amount
    [Documentation]    Set the amount for test data generation
    [Arguments]    ${AMOUNT}
    VAR    ${AMOUNT}    ${AMOUNT}    scope=test

Set Country
    [Documentation]    Set the country for test data generation
    [Arguments]    ${COUNTRY}
    VAR    ${COUNTRY}    ${COUNTRY}    scope=test

Set Format
    [Documentation]    Set the format for test data generation
    [Arguments]    ${FORMAT}
    VAR    ${FORMAT}    ${FORMAT}    scope=test

Set Temperature
    [Documentation]    Set the temperature for test data generation
    [Arguments]    ${TEMPERATURE}
    VAR    ${TEMPERATURE}    ${TEMPERATURE}    scope=test

Set Max Tokens
    [Documentation]    Set the maximum number of tokens for test data generation
    [Arguments]    ${MAX_TOKENS}
    VAR    ${MAX_TOKENS}    ${MAX_TOKENS}    scope=test

Set Top P
    [Documentation]    Set the top P value for test data generation
    [Arguments]    ${TOP_P}
    VAR    ${TOP_P}    ${TOP_P}    scope=test

Set Frequency Penalty
    [Documentation]    Set the frequency penalty for test data generation
    [Arguments]    ${FREQUENCY_PENALTY}
    VAR    ${FREQUENCY_PENALTY}    ${FREQUENCY_PENALTY}    scope=test

Set Presence Penalty
    [Documentation]    Set the presence penalty for test data generation
    [Arguments]    ${PRESENCE_PENALTY}
    VAR    ${PRESENCE_PENALTY}    ${PRESENCE_PENALTY}    scope=test
