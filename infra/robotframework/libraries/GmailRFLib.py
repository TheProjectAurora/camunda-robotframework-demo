from googleapiclient.discovery import build
from oauth2client import file, client, tools
from google.oauth2.credentials import Credentials
from httplib2 import Http
from email.mime.text import MIMEText
from apiclient import errors, discovery
from robot.api.deco import keyword
import logging
import base64
import sys


class GmailRFLib:
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self,token=None):
        try:
            creds = Credentials.from_authorized_user_file("/app/credentials/token.json", ["https://www.googleapis.com/auth/gmail.modify"])
            self.service = build("gmail", "v1", credentials=creds)
        except Exception as e:
            logging.exception(f"Error when initializing service:{e}")

    @keyword
    def send_results_search_email(self, to, subject, result_bing, result_duck, result_cows):
        try:
            message_text ="""
            <p> Bing: {bing}</p>
            <p> DuckDuckGo: {duck}</p>
            <p> Swisscows: {cows}</p><br/>""".format(bing=result_bing,duck=result_duck,cows=result_cows)
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