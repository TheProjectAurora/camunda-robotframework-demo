*** Settings ***
Resource     ..${/}resources${/}camunda_demo_resource.robot
Suite Setup  Fetch Task  ${TOPIC}

*** Tasks ***
Search with Bing
    [Tags]    search_bing
    [Setup]  Init Browser
    [Teardown]  Fail Task Randomly
    New page  http://www.bing.fi
    Type text  id=sb_form_q  ${VARS['search_term']}  delay=50 ms
    Click  xpath=//*[contains(@class, 'search')]
    Wait for elements state  id=b_results
    ${link_text}  Get text  xpath=//h2/a
    Set process variable  result_bing  ${link_text}

Search with DuckDuckGo
    [Tags]    search_duck
    [Setup]  Init Browser
    New page  https://duckduckgo.com
    Wait for elements state  id=search_form_input_homepage
    Type text  id=search_form_input_homepage  ${VARS['search_term']}  delay=50 ms
    Click  id=search_button_homepage
    Wait for elements state  id=links
    ${link_text}  Get text  xpath=//h2/a
    Set process variable  result_duck  ${link_text}

Search with Swisscows
    [Tags]    search_cows
    [Setup]  Init Browser
    New page  https://swisscows.com/
    Type text  xpath=//*[@class='input-search']  ${VARS['search_term']}  delay=50 ms
    Click  xpath=//*[@class='search-submit']
    Wait for elements state  xpath=//*[@class='web-results']
    ${link_text}  Get text  xpath=//*[@class='item item--web']/a/h2
    Set process variable  result_cows  ${link_text}

Send Search Result Email
    [Tags]    send_results
    Send results email