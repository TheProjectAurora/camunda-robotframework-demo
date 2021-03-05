*** Settings ***
Library         CamundaLibrary  ${CAMUNDA_HOST}
Library         Browser
Library         Collections
Suite Setup     Init Browser
Suite Teardown  Close Browser
Test Setup      Fetch Task  ${TOPIC}
Test Teardown   Complete Task  result_set=${RETURN_VALUES}

*** Variables ***
${CAMUNDA_HOST}
${TOPIC} 

*** Tasks ***
Search with Bing
    [Tags]    search_bing
    New page  http://www.bing.fi
    Type Text  id=sb_form_q  ${VARIABLES['search_term']}  delay=50 ms
    Click  xpath=//*[contains(@class, 'search')]
    Wait For Elements State  id=b_results
    ${link_text}  Get Text  xpath=//h2/a
    Set to dictionary  ${RETURN_VALUES}  result_bing=${link_text}

Search with DuckDuckGo
    [Tags]    search_duck
    New page  https://duckduckgo.com
    Wait for elements state  id=search_form_input_homepage
    Type text  id=search_form_input_homepage  ${VARIABLES['search_term']}  delay=50 ms
    Click  id=search_button_homepage
    Wait for elements state  id=links
    ${link_text}  Get text  xpath=//h2/a
    Set to dictionary  ${RETURN_VALUES}  result_duck=${link_text}

*** Keywords ***
Fetch Task
    [Arguments]    ${topic}
    ${variables}  Fetch workload  ${topic}
    ${return_values}  Create dictionary
    Set test variable  ${VARIABLES}  ${variables}
    Set test variable  ${RETURN_VALUES}  ${return_values}

Init Browser
    New browser  headless=true
    New context