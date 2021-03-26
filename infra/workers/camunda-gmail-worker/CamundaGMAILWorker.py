import re
import requests
import sys
import json
import time

class CamundaGMAILWorker:

    def __init__(self,camunda_url,poll_interval=5):
        self.subject_to_look = "search"
        self.msg_start_search = "start_search_process"
        self.engine = camunda_url+"/engine-rest"
        self.poll_interval = poll_interval
        self.mailhog_url = "http://localhost:8025"

    def poll_inbox_and_send_message_to_camunda(self):
        """
        Polls gmail inbox for new messages. If criterias are met, sends message to camunda engine to
        start process and marks email as read.
        """
        try:
            messages = requests.get(self.mailhog_url+"/api/v1/messages", verify=False)
            for msg in messages.json():
                email_valid = self._check_email_subject(msg)
                if email_valid:
                    self._send_message_to_engine_start_search()
                    self.requests.delete(self.mailhog_url+"/api/v1/messages/"+msg["ID"], verify=False)
        except Exception as e:
            print(f"Error when checking inbox messages:{e}")

    def _send_message_to_engine_start_search(self):
        """
        Sends start_search_process message to camunda engine
        """
        url = self.engine+"/message"
        headers = {"Content-type": "application/json"}
        payload = {
            "messageName" : self.msg_start_search,
            "processVariables" : {
            "subject" : {"value" : self.subject, "type": "String"},
            "search_term" : {"value" : self.search_term, "type": "String"},
            "result_duck" : {"value" : None, "type": "String"},
            "result_bing" : {"value" : None, "type": "String"},
            "result_cows" : {"value" : None, "type": "String"}}
            }
        try:
            r = requests.post(url, json=payload, headers=headers, verify=False)
            r.raise_for_status()
            print(f"Message sent to engine: {self.msg_start_search}")
        except Exception as e:
            print(f"Could not send message to engine: {e}")

    def _check_email_subject(self,msg):
        """
        Checks message if the criterias are met. If so, 
        sets process variables and returns true
        """
        subject = msg["Content"]["Headers"]["Subject"]
        if self.subject_to_look in subject:
            self.search_term = msg["Content"]["Body"]
            self.subject = subject
            print(f"Got {self.subject_to_look}! Search term: {self.search_term}")
            return True
        return False

if __name__ == "__main__":
    if len(sys.argv) != 1:
        t = CamundaGMAILWorker(sys.argv[1])
        while True:
            t.poll_inbox_and_send_message_to_camunda()
            time.sleep(t.poll_interval)
    else:
        sys.exit("Camunda url missing")