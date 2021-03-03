import re
import requests
import sys
import json
import time
try:
    import libraries.GmailLib as g
except Exception as e:
    print(f"Error when importing GmailLib:{e}")


class CamundaGMAILWorker:

    def __init__(self,camunda_url):
        self.sender_email_to_look = "@northcode.fi"
        self.subject_to_look = "Search"
        self.camunda_message = "start_search_process"
        self.camunda_engine_rest_url = camunda_url+"/engine-rest"
        self.gmail = g.GmailLib()

    def poll_inbox_and_send_message_to_camunda(self):
        """
        Polls gmail inbox for new messages. If criterias are met, sends message to camunda engine to
        start process and marks email as read.
        """
        try:
            results = self.gmail.fetch_unread_messages()
            messages = results.get("messages", [])
            if not messages:
                time.sleep(10)
            else:
                for msg in messages:
                    msg = self.gmail.get_message(msg["id"])
                    email_valid = self._check_email_subject_and_sender(msg)
                    if email_valid:
                        self._send_message_to_camunda_engine(self.sender_email, self.subject, self.search_term)
                        self.gmail.mark_email_as_read(msg["id"])
            return None
        except Exception as e:
            print(f"Error when checking inbox messages:{e}")

    def _send_message_to_camunda_engine(self, sender, subject, search_term):
        """
        Sends message to camunda engine to start process
        """
        url = self.camunda_engine_rest_url+"/message"
        headers = {"Content-type": "application/json"}
        payload = {
            "messageName" : self.camunda_message,
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
            print(f"Message sent to camunda engine: {self.camunda_message}")
        except Exception as e:
            print(f"Could not send message to camunda engine: {e}")

    def _check_email_subject_and_sender(self,msg):
        """
        Checks message if the criterias are met. If so, 
        sets camunda process variables and returns true
        """
        headers=msg["payload"]["headers"]
        subject = [i["value"] for i in headers if i["name"]=="Subject"] 
        sender = [i["value"] for i in headers if i["name"]=="From"]
        email = re.search(r"(?<=<).*?(?=>)", sender[0]).group(0)
        if self.subject_to_look in subject and self.sender_email_to_look in email:
            self.search_term = msg["snippet"]
            self.subject = subject
            self.sender_email = email
            print(f"Got {self.subject_to_look} mail from {self.sender_email_to_look}! Search term: {search_term}")
            return True
        return False

if __name__ == "__main__":
    print(f"Camunda url: {sys.argv[1]}")
    c = CamundaGMAILWorker(sys.argv[1])
    while True:
        c.poll_inbox_and_send_message_to_camunda()