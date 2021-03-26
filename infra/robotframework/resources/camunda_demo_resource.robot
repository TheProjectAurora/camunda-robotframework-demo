*** Settings ***
Library  CamundaLibrary  ${CAMUNDA_HOST}
Library  Browser
Library  Collections
Library  String

*** Keywords ***
Init Browser
    New browser  headless=true
    New context

Send Results Email
    Send results search email  Search results for ${VARS['search_term']}
    ...    ${VARS['result_bing']}  ${VARS['result_duck']}  ${VARS['result_cows']}
    Set Process Variable  results_sent  true

Fetch Task
    [Arguments]    ${topic}
    ${variables}  Fetch workload  ${topic}  
    ${resp}  Get fetch response
    ${return_values}  Create dictionary
    Set suite variable  ${WORKER_ID}  ${resp['worker_id']}
    Set suite variable  ${TASK_ID}  ${resp['id']}
    Set suite variable  ${VARS}  ${variables}
    Set suite variable  ${RETURN}  ${return_values}

Set Process Variable
    [Arguments]  ${key}  ${value}
    Set to dictionary  ${RETURN}  ${key}=${value}

Fail Task Randomly
    ${random}  Generate random string  1  [NUMBERS]
    Run keyword if  ${random} == 8  FAIL  Random Fail Happened!
