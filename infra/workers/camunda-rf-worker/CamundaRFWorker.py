from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.external_task.external_task_worker import ExternalTaskWorker
import robot
import requests
import sys
import time
import docker
import traceback
try:
    import libraries.GmailLib as g
except Exception as e:
    print(f"Error when importing GmailLib:{e}")


class CamundaRFWorker:

    def __init__(self,camunda_url):
        self.topics_to_subscribe = ("search_duck","search_bing","reply_result")
        self.robot_file = "CamundaDemoTasks.robot"
        self.worker_id = "1"
        self.camunda_url = camunda_url
        self.camunda_engine_rest_url = self.camunda_url+"/engine-rest"
        self.gmail = g.GmailLib()
        self.docker_client = docker.from_env()
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
        task_id = task.get_task_id()
        if topic in ("search_duck","search_bing"):
            print(f"Start robot framework task: {topic}")
            try:
                self._release_task(task_id)
                self.docker_client.containers.run("camunda-robotframework-demo_robotframework:latest",network="camunda-robotframework-demo_default",command="robot -d /tmp -i "+topic+" -v TOPIC:"+topic+" -v CAMUNDA_HOST:"+self.camunda_url+" /tmp")
            except Exception as e:
                print(f"Could not complete robot framework task: {e}")
                traceback.print_exc()
        else:
            try:
                print(f"Start task: {topic}")
                self._send_results_email_task(task)
            except Exception as e:
                print(f"Could not complete task: {e}")
                return task.failure(error_message="task failed",  error_details=str(e))
            print(f"Task completed: {topic}")
            return task.complete({"results_sent": True})
        return None

    def _send_results_email_task(self,task):
        sender = task.get_variable("sender")
        result_bing = task.get_variable("result_bing")
        result_duck = task.get_variable("result_duck")
        search_term = task.get_variable("search_term")
        message_text ='''
        <p> Bing: {bing}</p>
        <p> DuckDuckGo: {duck}</p><br/>BR,<br/>N<>rthC<>de'''.format(bing=result_bing,duck=result_duck)
        try:
            self.gmail.send_email(sender, "Search results for "+search_term, message_text)
        except Exception as e:
            print(f"Could not send results: {e}")

    def _release_task(self,id):
        """
        Release external task. Task is locked again by Robot framework
        """
        try:
            url = self.camunda_engine_rest_url+"/external-task/"+id+"/unlock"
            headers = {"Content-type": "application/json"}
            r = requests.post(url, headers=headers)
            r.raise_for_status()
            print(f"Task released: {id}")
        except Exception as e:
            print(f"Could not release task: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 1:
        t = CamundaRFWorker(sys.argv[1])
        ExternalTaskWorker(base_url=t.camunda_engine_rest_url,config=t.default_config,worker_id=t.worker_id).subscribe(t.topics_to_subscribe, t.handle_task)
    else:
        sys.exit("Camunda url missing")