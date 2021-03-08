from googleapiclient.discovery import build
from oauth2client import file, client, tools
from httplib2 import Http
from email.mime.text import MIMEText
from apiclient import errors, discovery
from robot.api.deco import keyword
import logging
import base64
import sys


class GmailRFLib:
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

    def __init__(self,token=None,creds=None):
        try:
            creds = file.Storage("/tmp/credentials/token.json").get()
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets("/tmp/credentials/credentials.json", SCOPES)
                creds = tools.run_flow(flow, store)
            self.service = build("gmail", "v1", http=creds.authorize(Http()))
        except Exception as e:
            logging.exception(f"Error when initializing service:{e}")

    @keyword
    def send_result_email(self, to, subject, results):
        try:
            message_text ="""
            <p> Bing: {bing}</p>
            <p> DuckDuckGo: {duck}</p><br/>BR,<br/>N<>rthC<>de""".format(bing=results,duck=results)
            message = self._create_message(to, subject, message_text)
            r = self.service.users().messages().send(userId="me", body=message).execute()
            logging.info(f"Email sent: {r}")
        except errors.HttpError as error:
            logging.exception(f"Could not send email: {error}")

    def _create_message(self, to, subject, message_text):
        message = MIMEText(message_text,"html")
        message["to"] = to
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {"raw": raw}
        return body  