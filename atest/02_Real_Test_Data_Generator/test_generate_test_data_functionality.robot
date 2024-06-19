*** Settings ***
Documentation    Tests the functionality of the generate test data keyword
Library    Collections
Library    ../../src/RobotFrameworkAI/modules/real_test_data_generator/RealTestDataGenerator.py


*** Variables ***
${AI_MODEL}            openai
${TYPE}                phone_number
${MODEL}               gpt-3.5-turbo
${AMOUNT}              3
${FORMAT}              "{'addresses':[{'address': address}]}"
${MAX_TOKENS}          256
${TEMPERATURE}         1
${TOP_P}               1
${FREQUENCY_PENALTY}   0
${PRESENCE_PENALTY}    0
${COUNTRY}             Czech Republic
${GENERATED_TEST_DATA}    ${EMPTY}


*** Test Cases ***
Acceptance Test: Generate Test Data
    [Documentation]    Verify the behavior of generate_test_data keyword with various input arguments
    [Tags]    acceptance
    When Generate Test Data
    Then Test Data Is Generated Successfully
    And Test Data Is In Right Format    ${AMOUNT}


*** Keywords ***
When Generate Test Data
    [Documentation]    Generate test data
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
    VAR    ${GENERATED_TEST_DATA}    ${test_data}    scope=test

Then Test Data Is Generated Successfully
    [Documentation]    Check if keyword returned a non-empty list
    Should Not Be Empty    ${GENERATED_TEST_DATA}

And Test Data Is In Right Format
    [Documentation]    Check if the list has the right amount of elements
    [Arguments]    ${expected_amount}
    ${actual_amount} =    Get Length    ${GENERATED_TEST_DATA}
    Should Be Equal As Numbers    ${actual_amount}    ${expected_amount}