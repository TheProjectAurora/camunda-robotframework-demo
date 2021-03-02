*** Settings ***
Library        CamundaLibrary.ExternalTask  ${CAMUNDA_HOST}
Library        Browser
Library        Collections
Test Setup     Lock Workload and Fetch Task  ${TOPIC}
Test Teardown  Complete Task  ${TOPIC}  ${RECENT_TASK}  ${VARIABLES}

*** Variables ***
${CAMUNDA_HOST}  http://localhost:8080
${SLEEP}         1  

*** Test Cases ***
Search with Bing
    [Tags]    search_bing
    Open Browser  http://www.bing.fi  headless=${True}
    Type Text  id=sb_form_q  ${VARIABLES['search_term']['value']}  delay=50 ms
    Click  xpath=//*[contains(@class, 'search')]
    Wait For Elements State  id=b_results
    ${link_text}  Get Text  xpath=//h2/a
    Set Test Message  ${VARIABLES['search_term']['value']}\n${link_text}
    Set To Dictionary  ${VARIABLES['result_bing']}  value=${link_text}
    #Add some sleep to see where token goes in camunda cockpit
    Sleep  ${SLEEP} seconds

Search with DuckDuckGo
    [Tags]    search_duck
    Open browser  https://duckduckgo.com  headless=${True}
    Wait for elements state  id=search_form_input_homepage
    Type text  id=search_form_input_homepage  ${VARIABLES['search_term']['value']}  delay=50 ms
    Click  id=search_button_homepage
    Wait for elements state  id=links
    ${link_text}  Get text  xpath=//h2/a
    Set Test Message  ${VARIABLES['search_term']['value']}\n${link_text}
    Set to dictionary  ${VARIABLES['result_duck']}  value=${link_text}
    #Add some sleep to see where token goes in camunda cockpit
    Sleep  ${SLEEP} seconds

*** Keywords ***
Lock Workload and Fetch Task
    [Arguments]    ${topic_name}
    &{variables}  Fetch and Lock workloads  ${topic_name}
    ${recent_task}  Get recent process instance
    Set test variable  &{VARIABLES}  &{variables}
    Set test variable  ${RECENT_TASK}  ${recent_task}
    Log  Task ID:\t${recent_task}