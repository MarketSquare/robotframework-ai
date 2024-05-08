*** Settings ***
Documentation    Example usage of the generate test data keyword
...    Generates 3 addresses to search on google map
Library    OperatingSystem
Library    ../../modules/real_test_data_generator/RealTestDataGenerator.py
Library    SeleniumLibrary


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
Generate 3 Addresses And Search Them On Google Maps
    [Documentation]    Generates addresses and searches them on google maps
    Open Maps
    Setup Test Parameters
    Set Country    Czech Republic

    @{ADDRESSES}    Generate Test Data With Parameters

    FOR    ${address}    IN    @{ADDRESSES}
        Search Address    ${address}
        Sleep    5
    END


*** Keywords ***
Setup Test Parameters
    [Documentation]    Set default test parameters
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

Search Address
    [Documentation]    Inputs address in google maps search field and clicks search
    [Arguments]    ${SEARCH_QUERY}
    Input Text    //input[@id='searchboxinput']    ${SEARCH_QUERY}
    Wait Until Element Is Visible    //button[@id='searchbox-searchbutton']
    Click Button    //button[@id='searchbox-searchbutton']

Open Maps
    [Documentation]    Opens chrome, accepts cookies and opens google maps
    Open Browser    https://google.com    Chrome
    Click Button    //button[@id='L2AGLb']
    Go To    https://maps.google.com

Generate Test Data With Parameters
    [Documentation]    Generates test data using the specified parameters
    ${test_data}    Generate Test Data
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
