from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from email.mime.text import MIMEText
from apiclient import errors, discovery
import re
import requests
import sys
import logging
import json
import base64
import time

logging.getLogger("googleapicliet.discovery_cache").setLevel(logging.ERROR)
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

class CamundaGMAILWorker:

    def __init__(self,camunda_url):
        self.sender_email_to_look = "@northcode.fi"
        self.subject_to_look = "Search"
        self.camunda_process_message = "start_search_process"
        self.camunda_engine_rest_url = camunda_url+"/engine-rest"
        try:
            creds = file.Storage("/app/token.json").get()
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets("/app/credentials.json", SCOPES)
                creds = tools.run_flow(flow, store)
            self.service = build("gmail", "v1", http=creds.authorize(Http()))
        except Exception as ex:
            print("Error when initializing service:"+str(ex))

    def poll_inbox(self):
        """
        Polls gmail inbox for new messages. If criterias are met, sends message to camunda engine to
        start process and marks email as read.

        """
        results = self.service.users().messages().list(userId="me",labelIds = ["INBOX","UNREAD"]).execute()
        messages = results.get("messages", [])
        if not messages:
            time.sleep(10)
        else:
            for msg in messages:
                msg = self.service.users().messages().get(userId="me", id=msg["id"]).execute()
                headers=msg["payload"]["headers"]
                subject = [i["value"] for i in headers if i["name"]=="Subject"]
                if self.subject_to_look in subject:
                    search_term = msg["snippet"]
                    sender = [i["value"] for i in headers if i["name"]=="From"]
                    sender_email = re.search(r"(?<=<).*?(?=>)", sender[0]).group(0)
                    if self.sender_email_to_look in sender_email:
                        print("Got "+self.subject_to_look+" mail from "+self.sender_email_to_look+"! Search: "+search_term)
                        self._send_message_to_camunda_engine(sender_email, subject, search_term)
                        self._mark_email_as_read(msg["id"])
        return None

    def send_email(self, to, subject, message_text):
        try:
            message = self._create_message(to, subject, message_text)
            r = self.service.users().messages().send(userId="me", body=message).execute()
            print("\n\nResults email sent!: "+str(r)+"\n\n")
        except errors.HttpError as error:
            print("Could not send email"+str(error))

    def _send_message_to_camunda_engine(self, sender, subject, search_term):
        url = self.camunda_engine_rest_url+"/message"
        headers = {"Content-type": "application/json"}
        payload = {
            "messageName" : self.camunda_process_message,
            "processVariables" : {
            "sender" : {"value" : sender, "type": "String"},
            "subject" : {"value" : subject, "type": "String"},
            "search_term" : {"value" : search_term, "type": "String"},
            "result_duck" : {"value" : None, "type": "String"},
            "result_bing" : {"value" : None, "type": "String"}}
            }
        try:
            r = requests.post(url, json=payload, headers=headers, verify=False)
            r.raise_for_status()
            print("Message sent to camunda engine:"+self.camunda_process_message)
        except Exception as ex:
            print("Could not send message to camunda engine: "+str(ex))

    def _mark_email_as_read(self, message_id):
        try:
            r = self.service.users().messages().modify(userId="me", id=message_id, body={"removeLabelIds": ["UNREAD"]}).execute()
            print(r)
            print("Email marked as read: "+message_id)
        except errors.HttpError as error:
            print("Could not mark email as read: "+message_id)

    def _create_message(self, to, subject, message_text):
        message = MIMEText(message_text,"html")
        message["to"] = to
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {"raw": raw}
        return body

if __name__ == "__main__":
    print("Camunda engine url:"+sys.argv[1])
    c = CamundaGMAILWorker(sys.argv[1])
    while True:
        c.poll_inbox()