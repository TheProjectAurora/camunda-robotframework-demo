from googleapiclient.discovery import build
from oauth2client import file, client, tools
from httplib2 import Http
from email.mime.text import MIMEText
from apiclient import errors, discovery
import base64
import sys

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

class GmailLib:

    def __init__(self,token=None,creds=None):
        try:
            creds = file.Storage("/app/credentials/token.json").get()
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets("/app/credentials/credentials.json", SCOPES)
                creds = tools.run_flow(flow, store)
            self.service = build("gmail", "v1", http=creds.authorize(Http()))
        except Exception as e:
            print(f"Error when initializing service:{e}")
            sys.exit(1)

    def fetch_unread_messages(self):
        messages = None
        try:
            messages = self.service.users().messages().list(userId="me",labelIds = ["INBOX","UNREAD"]).execute().get("messages", [])
            if len(messages) > 0:
                print(f"Messages found!")
        except Exception as e:
            print(f"Could not fetch messages: {e}")
        return messages

    def get_message(self, msg_id):
        try:
            result = self.service.users().messages().get(userId="me", id=msg_id).execute()
        except Exception as e:
            print(f"Could not get message: {e}")
        return result

    def send_email(self, to, subject, message_text):
        try:
            message = self._create_message(to, subject, message_text)
            r = self.service.users().messages().send(userId="me", body=message).execute()
            print(f"Email sent: {r}")
        except errors.HttpError as error:
            print(f"Could not send email: {error}")
    
    def mark_email_as_read(self, message_id):
        try:
            r = self.service.users().messages().modify(userId="me", id=message_id, body={"removeLabelIds": ["UNREAD"]}).execute()
            print(f"Email marked as read: {message_id}\n{r}")
        except errors.HttpError as error:
            print(f"Could not mark email as read: {message_id}\n{error}")

    def _create_message(self, to, subject, message_text):
        message = MIMEText(message_text,"html")
        message["to"] = to
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {"raw": raw}
        return body  