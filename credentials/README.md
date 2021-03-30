#  Save credentials to this folder before kick up demo
### camunda-robotframework-demo/credentials$ ls -1
```
README.md
credentials.json
token.json
```
# How to get gmail credentials:

- Go to https://console.cloud.google.com/
- Create / pick up project where to create account
- Go to "APIs & Services"
- Go to "API Librarys"
- Search "Gmail API", enable it with putton.
- Go back to "Go to "APIs & Services" and there to "OAuth consensus screen"
    - User type: External
    - App Name: Anything e.g. CamundaDemo
    - Support email: Same than your gmail user
    - Contact email addresses: Any email
- Then just "Save and Continue" many times even it ask something...
- Go back to "Go to "APIs & Services" and there to "OAuth consensus screen" and push "PUBLISH APP" button so Publishing status is "In production"
- Go back to "Go to "APIs & Services" and there to "Credentials" and "CREATE CREDENTIALS" where pickup "OAuth Client ID"
    - Application type: Descktop app
    - Name: Anything e.g. CamundaDemo
- Close pop up screen.
- Go back to "Go to "APIs & Services" and there to "Credentials" and in right side of windows is download button.
- Download client_secrets_diibadaaba.apps.googleusercontent.com.json and save it to camunda-robotframework-demo repo clone folder credentials/credentials.json file.
### cat credentials.json
```
{
    "installed": {
        "client_id": "<GOOGLE-CREDENTIAL-CLIENT-ID>.apps.googleusercontent.com",
        "project_id": "<GOOGLE-PROJECT>",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "<GOOGLE-CREDENTIAL-CLIENT-SECRET>",
        "redirect_uris": [
            "urn:ietf:wg:oauth:2.0:oob",
            "http://localhost"
        ]
    }
}
```
## NOTE! THIS PART REQUIRE PYTHON + BROWSER
- Get token.json generators:
```
wget https://raw.githubusercontent.com/googleworkspace/python-samples/master/gmail/quickstart/requirements.txt
wget https://raw.githubusercontent.com/googleworkspace/python-samples/master/gmail/quickstart/quickstart.py
```
-  Modify quickstart.py by execute: ```sed -i "s|gmail.readonly|gmail.modify|g" quickstart.py```
-  Execute: ```pip3 install -r requirements.txt```
-  Execute: ```python quickstart.py```
-  quickstart.py open browser automaticly and generate token.json. Browser says "The authentication flow has completed, you may close this window." when it get things done.

## token.json generated by quickstart.py
### cat token.json
```
{
    "token": "<TOKEN-BY-quickstart.py>",
    "refresh_token": "<TOKEN-BY-quickstart.py>",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "<GOOGLE-CREDENTIAL-CLIENT-ID>.apps.googleusercontent.com",
    "client_secret": "<GOOGLE-CREDENTIAL-CLIENT-SECRET>",
    "scopes": [
        "https://www.googleapis.com/auth/gmail.modify"
    ],
    "expiry": "2021-03-15T14:31:14.405410Z"
}
```