*** Settings ***
Documentation    Tests the functionality of the assistant module
Library    Collections
Library    ../../src/RobotFrameworkAI/modules/assistant/Assistant.py
Test Setup    Set Arguments
Test Teardown    Test Teardown


*** Test Cases ***
Acceptance Test: Full test run of the assistant
    [Documentation]    Create a full run of the assistant module.
    ...    1. Creates an assistant
    ...    2. Sets argument: Name, AI Model, Instructions, File Paths and Message
    ...    3. Attaches files to the assistant
    ...    4. Unset File Paths so it doesn't get send with the prompt aswell
    ...    5. Sends a prompt to the assistant
    ...    6. Log prompt
    ...    7. Get ID of active assistant
    ...    8. Set argument ID
    ...    9. Delete assistant
    [Tags]    acceptance
    Create Assistant
    Attach Files    file_paths= ["src/RobotFrameworkAI/objects"]
    ${response} =    Send Message
    Log    ${response}

Acceptance Test: Test assistant threads
    [Documentation]    Tests whether assistant threads work as intended.
    ...    Aslong as no new thread is created the assistant remembers what it has been told.
    ...    When a new thread is created, it should have no memories of it.
    [Tags]    acceptance
    Set Message    If I say Water you say Fire
    Create Assistant
    Send Message
    Set Message    Water
    Send Message
    Create New Thread
    Send Message


*** Keywords ***
Set Arguments
    [Documentation]    Sets argument used for the keywords
    Set Name    Test Assistant
    Set AI Model    openai
    Set Message    Can you tell me ?
    Set Instructions    Hi

Test Teardown
    [Documentation]    Unsets arguments and delete assistant
    ${id} =    Get Active Assistant Id
    Set Id    ${id}
    Delete Assistant
