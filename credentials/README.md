# Add these files to this folder:

## cat token.json
```
{
    "access_token": "DIIPADAAPA", 
    "client_id": "CLIENTID.apps.googleusercontent.com", 
    "client_secret": "DIIPADAAPA", 
    "refresh_token": "DIIPADAAPA", 
    "token_expiry": "2021-03-03T13:05:35Z", 
    "token_uri": "https://accounts.google.com/o/oauth2/token", 
    "user_agent": null, 
    "revoke_uri": "https://oauth2.googleapis.com/revoke", 
    "id_token": null, 
    "id_token_jwt": null, 
    "token_response": 
    {
        "access_token": "DIIPADAAPA", 
        "expires_in": 3599, 
        "scope": "https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.modify", 
        "token_type": "Bearer"
    }, "scopes": 
        [
            "https://www.googleapis.com/auth/gmail.readonly", 
            "https://www.googleapis.com/auth/gmail.modify"
        ], 
    "token_info_uri": "https://oauth2.googleapis.com/tokeninfo", 
    "invalid": false, 
    "_class": "OAuth2Credentials", 
    "_module": "oauth2client.client"
}
```
## cat credentials.json
```
{
  "web": {
    "client_id": "CLIENTID.apps.googleusercontent.com",
    "client_secret": "DIIPADAAPA",
    "redirect_uris": ["https://www.example.com/oauth2callback"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token"
  }
}
```