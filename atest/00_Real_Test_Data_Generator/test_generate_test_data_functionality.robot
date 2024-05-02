*** Settings ***
Library    Collections
Library    ../../ai_interface/modules/real_test_data_generator/RealTestDataGenerator.py

*** Variables ***
${VALID_AI_MODEL}            openai
${VALID_TYPE}                address
${VALID_AMOUNT}              3
${VALID_FORMAT}              "{'addresses':[{'address': address}]}"
${VALID_MAX_TOKENS}          256
${VALID_MODEL}               gpt-3.5-turbo
${VALID_TEMPERATURE}         1
${VALID_TOP_P}               1
${VALID_FREQUENCY_PENALTY}   0
${VALID_PRESENCE_PENALTY}    0
${VALID_COUNTRY}             Czech Republic

*** Test Cases ***
Acceptance Test: Generate Test Data
    [Documentation]    Verify the behavior of generate_test_data keyword with various input parameters
    [Tags]    acceptance
    Given Valid Input Parameters
    When Generate Test Data
    Then Test Data Is Generated Successfully
    And Test Data Is In Right Format    ${VALID_AMOUNT}

*** Keywords ***
Given Valid Input Parameters
    Set Test Variable    ${AI_MODEL}             ${VALID_AI_MODEL}
    Set Test Variable    ${TYPE}                 ${VALID_TYPE}
    Set Test Variable    ${AMOUNT}               ${VALID_AMOUNT}
    Set Test Variable    ${FORMAT}               ${VALID_FORMAT}
    Set Test Variable    ${MAX_TOKENS}           ${VALID_MAX_TOKENS}
    Set Test Variable    ${MODEL}                ${VALID_MODEL}
    Set Test Variable    ${TEMPERATURE}          ${VALID_TEMPERATURE}
    Set Test Variable    ${TOP_P}                ${VALID_TOP_P}
    Set Test Variable    ${FREQUENCY_PENALTY}    ${VALID_FREQUENCY_PENALTY}
    Set Test Variable    ${PRESENCE_PENALTY}     ${VALID_PRESENCE_PENALTY}
    Set Test Variable    ${COUNTRY}              ${VALID_COUNTRY}

When Generate Test Data
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
    Set Test Variable    ${GENERATED_TEST_DATA}    ${test_data}

Then Test Data Is Generated Successfully
    Should Not Be Empty    ${GENERATED_TEST_DATA}

And Test Data Is In Right Format
    [Arguments]    ${expected_amount}
    ${actual_amount} =    Get Length    ${GENERATED_TEST_DATA}
    Should Be Equal As Numbers    ${actual_amount}    ${expected_amount}
