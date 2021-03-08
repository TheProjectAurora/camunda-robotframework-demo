*** Settings ***
Library         CamundaLibrary  ${CAMUNDA_HOST}
Library         Browser
Library         Collections
Library         GmailRFLib
Suite Setup     Init Browser
Test Setup      Fetch Task  ${TOPIC}

*** Variables ***
${CAMUNDA_HOST}
${TOPIC} 

*** Tasks ***
Search with Bing
    [Tags]    search_bing
    New page  http://www.bing.fi
    Type Text  id=sb_form_q  ${VARS['search_term']}  delay=50 ms
    Click  xpath=//*[contains(@class, 'search')]
    Wait For Elements State  id=b_results
    ${link_text}  Get Text  xpath=//h2/a
    Set to dictionary  ${RETURN}  result_bing=${link_text}

Search with DuckDuckGo
    [Tags]    search_duck
    New page  https://duckduckgo.com
    Wait for elements state  id=search_form_input_homepage
    Type text  id=search_form_input_homepage  ${VARS['search_term']}  delay=50 ms
    Click  id=search_button_homepage
    Wait for elements state  id=links
    ${link_text}  Get text  xpath=//h2/a
    Set to dictionary  ${RETURN}  result_duck=${link_text}

Send Search Result Email
    [Tags]    send_results
    Send result email  ${VARS['sender']}  ${VARS['search_term']}  ${VARS['result_duck']}
    Set to dictionary  ${RETURN}  results_sent=true

*** Keywords ***
Fetch Task
    [Arguments]    ${topic}
    ${variables}  Fetch workload  ${topic}  
    ${resp}  Get fetch response
    ${return_values}  Create dictionary
    Set test variable  ${WORKER_ID}  ${resp['worker_id']}
    Set test variable  ${TASK_ID}  ${resp['id']}
    Set test variable  ${VARS}  ${variables}
    Set test variable  ${RETURN}  ${return_values}

Init Browser
    New browser  headless=true
    New context