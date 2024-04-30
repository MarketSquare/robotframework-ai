*** Settings ***
Library    ai_interface/modules/real_test_data_generator/RealTestDataGenerator.py
Library    SeleniumLibrary

*** Test Cases ***
Execute Generate 3 Addresses And Search Them On Google Maps
   Open Maps
   Set AI Model    openai
   Set Count    3
   Set Country    Czech Republic
   Set Format    "{'addresses':[{'address': address}]}"
   Set Max Tokens    256
   Set Model    gpt-3.5-turbo
   Set Temperature    1
   Set Top P    1
   Set Frequency Penalty    0
   Set Presence Penalty    0

   Set Addresses   
    
   FOR    ${address}    IN    @{ADDRESSES}
        Search Address    ${address}
        Sleep    5
   END
   Log    Test execution finished

*** Keywords ***

Search Address
    [Arguments]    ${SEARCH_QUERY}
    Input Text    //input[@id='searchboxinput']    ${SEARCH_QUERY}
    Wait Until Element Is Visible    //button[@id='searchbox-searchbutton']
    Click Button    //button[@id='searchbox-searchbutton']

Enter Search Query
    [Arguments]    ${SEARCH_QUERY}
    Input Text    //textarea    ${SEARCH_QUERY}

Open Maps
    Open Browser    https://google.com    Chrome
    Click Button    //button[@id='L2AGLb']
    Go To    https://maps.google.com

Set Addresses
    @{addresses}=    Generate Test Addresses    ${AI_MODEL}    ${COUNT}    ${COUNTRY}    ${FORMAT}    ${MAX_TOKENS}
    ...    ${MODEL}    ${TEMPERATURE}    ${TOP_P}    ${FREQUENCY_PENALTY}    ${PRESENCE_PENALTY}
    Set Test Variable    @{ADDRESSES}    @{addresses}

Set AI Model
    [Arguments]    ${ai_model}
    Set Test Variable    ${AI_MODEL}    ${ai_model}

Set Count
    [Arguments]    ${count}
    Set Test Variable    ${COUNT}    ${count}

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
   

