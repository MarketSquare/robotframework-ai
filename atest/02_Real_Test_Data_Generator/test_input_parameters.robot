*** Settings ***
Documentation    Tests the input validation for the keyword generate test data
Library    ../../src/RobotFrameworkAI/modules/real_test_data_generator/RealTestDataGenerator.py
Suite Setup    Setup Test Arguments


*** Test Cases ***
Test Invalid AI Model
    [Documentation]    Test when AI Model is invalid
    Set AI Model    invalid_model
    Run Keyword And Expect Error    ValueError: *    Generate Test Data

Test Invalid Type
    [Documentation]    Test when Type is invalid
    Set Type    invalid_type
    Run Keyword And Expect Error    ValueError: *    Generate Test Data

Test Invalid Model
    [Documentation]    Test when Model is invalid
    Set Model    invalid_model    # Set invalid Model value
    Run Keyword And Expect Error    ValueError: *    Generate Test Data

Test Invalid Max Tokens
    [Documentation]    Test when Max Tokens is invalid
    Set Max Tokens    5000    # Set invalid Max Tokens value
    Run Keyword And Expect Error    ValueError: *    Generate Test Data

Test Invalid Temperature
    [Documentation]    Test when Temperature is invalid
    Set Temperature    -1.5    # Set invalid Temperature value
    Run Keyword And Expect Error    ValueError: *    Generate Test Data

Test Invalid Top P
    [Documentation]    Test when Top P is invalid
    Set Top P    2.5    # Set invalid Top P value
    Run Keyword And Expect Error    ValueError: *    Generate Test Data

Test Invalid Frequency Penalty
    [Documentation]    Test when Frequency Penalty is invalid
    Set Frequency Penalty    -3.0    # Set invalid Frequency Penalty value
    Run Keyword And Expect Error    ValueError: *    Generate Test Data

Test Invalid Presence Penalty
    [Documentation]    Test when Presence Penalty is invalid
    Set Presence Penalty    3.0    # Set invalid Presence Penalty value
    Run Keyword And Expect Error    ValueError: *    Generate Test Data

Test All Valid
    [Documentation]    Test when all arguments are valid
    Setup Test Arguments
    Generate Test Data

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
    Run Keyword And Expect Error    ValueError: *    Generate Test Data


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
    Set Top P    .5
    Set Frequency Penalty    0
    Set Presence Penalty    0
    Set Kwarg    country    Czech Republic
