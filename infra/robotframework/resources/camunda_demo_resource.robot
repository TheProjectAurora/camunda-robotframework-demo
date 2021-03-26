*** Settings ***
Library  CamundaLibrary  ${CAMUNDA_HOST}
Library  RequestsLibrary
Library  Browser
Library  Collections
Library  ../libraries/GmailRFLib.py

*** Keywords ***
Init Browser
    New browser  headless=true
    New context

Send Results Email
    Send results search email  ${VARS['sender']}  Search results for ${VARS['search_term']}
    ...    ${VARS['result_bing']}  ${VARS['result_duck']}  ${VARS['result_cows']}
    Set Process Variable  results_sent  true

Send error result email
    ${fetch_response}    Get fetch response
    Create Session    camunda    ${CAMUNDA_HOST}
    ${response}    Get On Session    camunda    /engine-rest/task?processInstanceId=${fetch_response}[process_instance_id]    expected_result=200
    ${task_id}    Set Variable    ${response}[id]
    ${task_url}    Set Variable    ${CAMUNDA_HOST}/camunda/app/tasklist/default/#/?task=${task_id}
    Send results search email  ${VARS['sender']}  Search results error
    ...    Check this cool error out: ${task_url}


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
