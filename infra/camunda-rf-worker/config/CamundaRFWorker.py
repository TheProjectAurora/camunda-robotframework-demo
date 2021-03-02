from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.external_task.external_task_worker import ExternalTaskWorker
import CamundaGMAILWorker as g
import robot
import requests
import sys
import time

class CamundaRFWorker:

    def __init__(self,camunda_url):
        self.topics_to_subscribe = ("search_duck","search_bing","reply_result")
        self.robot_file = "CamundaDemoTasks.robot"
        self.worker_id = "1"
        self.camunda_url = camunda_url
        self.default_config = {
            "maxTasks": 1,
            "lockDuration": 10000,
            "asyncResponseTimeout": 5000,
            "retries": 2,
            "retryTimeout": 5000,
            "sleepSeconds": 30
            }

    def handle_task(self,task: ExternalTask) -> TaskResult:
        """
        This task handler you need to implement with your business logic.
        After completion of business logic call either task.complete() or task.failure() or task.bpmn_error() 
        to report status of task to Camunda
        """
        topic = task.get_topic_name()
        taskId = task.get_task_id()
        if topic in ("search_duck","search_bing"):
            logFile = open(topic+"_"+taskId+".txt", "w")
            self._release_task(taskId)
            robot_run = robot.run(self.robot_file,variable="topic:"+topic,include=[topic],stdout=logFile,report=topic+"_"+taskId+".html")
            self._print_info_to_console(logFile.name)
        else:
            self._send_results_email_task(task)
            return task.complete({"results_sent": True})
        return None

    def _send_results_email_task(self,task):
        sender = task.get_variable("sender")
        result_bing = task.get_variable("result_bing")
        result_duck = task.get_variable("result_duck")
        search_term = task.get_variable("search_term")
        message_text ='''
        <p> Bing: {bing}</p>
        <p> DuckDuckGo: {duck}</p><br/>BR,<br/>Jaska'''.format(bing=result_bing,duck=result_duck)
        try:
            g.GmailCamunda().send_email(sender, "Search results for "+search_term, message_text)
        except Exception as ex:
            print("Could not send results: "+str(ex))

    def _release_task(self,id):
        """
        Release external task. Task is locked again by Robot framework

        """
        try:
            url = self.camunda_url+"/engine-rest/external-task/"+id+"/unlock"
            headers = {"Content-type": "application/json"}
            r = requests.post(url, headers=headers)
            r.raise_for_status()
            print("Task released:"+id)
        except Exception as ex:
            print("Could not release task: "+str(ex))

    def _print_info_to_console(self,log_file):
        with open(log_file, "r", encoding="utf8") as read_obj:
            for line in read_obj:
                print(line)
        #Add some sleep just to see logs in console
        time.sleep(5)
        return None

if __name__ == '__main__':
    print("Camunda url:"+sys.argv[1])
    t = CamundaRFWorker(sys.argv[1])
    ExternalTaskWorker(config=t.default_config,worker_id=t.worker_id).subscribe(t.topics_to_subscribe, t.handle_task)