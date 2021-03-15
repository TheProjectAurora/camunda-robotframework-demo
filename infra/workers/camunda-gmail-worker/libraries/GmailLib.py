from googleapiclient.discovery import build
from httplib2 import Http
from email.mime.text import MIMEText
from apiclient import errors
from google.oauth2.credentials import Credentials
import base64
import sys


class GmailLib:

    def __init__(self,token=None):
        try:
            creds = Credentials.from_authorized_user_file("/credentials/token.json", ["https://www.googleapis.com/auth/gmail.modify"])
            self.service = build("gmail", "v1", credentials=creds)
        except Exception as e:
            print(f"Error when initializing service:{e}")
            sys.exit(1)

    def fetch_unread_messages(self):
        messages = None
        try:
            messages = self.service.users().messages().list(userId="me",labelIds = ["INBOX","UNREAD"]).execute().get("messages", [])
            msg_count = len(messages)
            print(f"{msg_count} message(s) found from mailbox",flush=True)
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