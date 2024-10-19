*** Settings ***
Documentation    Tests the functionality of the generate test data keyword
Library    Collections
Library    ../../src/RobotFrameworkAI/modules/real_test_data_generator/RealTestDataGenerator.py
Library    ../../src/RobotFrameworkAI/logger/logger.py


*** Variables ***
${AI_MODEL}            openai
${TYPE}                address
${MODEL}               gpt-3.5-turbo
${AMOUNT}              3
${FORMAT}              "{'addresses':[{'address': address}]}"
${MAX_TOKENS}          256
${TEMPERATURE}         1
${TOP_P}               1
${FREQUENCY_PENALTY}   0
${PRESENCE_PENALTY}    0
${COUNTRY}             Czech Republic

*** Test Cases ***
Acceptance Test: Generate Test Data
    [Documentation]    Verify the behavior of generate_test_data keyword with various input arguments
    [Tags]    acceptance
    Setup Logging
    Set AI Model    ${AI_MODEL}
    Set Type    ${TYPE}
    Set Model    ${MODEL}
    Set Amount    ${AMOUNT}
    Set Format    ${FORMAT}
    Set Max Tokens    ${MAX_TOKENS}
    Set Temperature    ${TEMPERATURE}
    Set Top P    ${TOP_P}
    Set Frequency Penalty    ${FREQUENCY_PENALTY}
    Set Presence Penalty    ${PRESENCE_PENALTY}

    ${test_data}=    When Generate Test Data
    Then Test Data Is Generated Successfully    ${test_data}
    And Test Data Is In Right Format    ${test_data}    ${AMOUNT}


*** Keywords ***
When Generate Test Data
    [Documentation]    Generate test data
    ${test_data} =    Generate Test Data    country=${COUNTRY}
    RETURN    ${test_data}

Then Test Data Is Generated Successfully
    [Documentation]    Check if keyword returned a non-empty list
    [Arguments]    ${test_data}
    Should Not Be Empty    ${test_data}

And Test Data Is In Right Format
    [Documentation]    Check if the list has the right amount of elements
    [Arguments]    ${test_data}    ${expected_amount}
    ${actual_amount} =    Get Length    ${test_data}
    Should Be Equal As Numbers    ${actual_amount}    ${expected_amount}
