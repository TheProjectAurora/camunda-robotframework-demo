import requests
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot import rebot
import owncloud
import random
import time

"""Camunda listener takes care of task status update to engine
"""
class NotFound(Exception):
    pass

class CamundaListener:
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, camunda_url):
        self.camunda_url = camunda_url
        self.engine = self.camunda_url+"/engine-rest"
        self.result_set = []
        self.test_status = True
        try:
            self.oc_client = owncloud.Client("http://owncloud:8080")
            self.oc_client.login("demo","demo")
        except Exception as e:
            logger.error(f"Error when creating cloud instance: {e}")

    def end_test(self, data, result):
        try:
            self.task_id = BuiltIn().get_variable_value("${TASK_ID}")
            self.worker_id = BuiltIn().get_variable_value("${WORKER_ID}")
            self.test_message = BuiltIn().get_variable_value("${TEST_MESSAGE}")
            self._set_task_completed_variables()
            if result.passed:
                self.test_status = True
            else:
                self.test_status = False
        except Exception as e:
            logger.error(f"Error when end test happened: {e}")

    def close(self):
        try:
            report_url = self._upload_results()
            if self.test_status:
                self._complete_task(report_url)
            else:
                self._fail_task()
        except Exception as e:
            logger.error(f"Error when close happened: {e}")
    
    def output_file(self, path):
        self.output_file = path

    def log_file(self, path):
        self.log_file = path

    def report_file(self, path):
        self.report_file = path

    def _complete_task(self, robot_results_url):
        """
        Sends task complete to engine
        """
        try:
            url = self.engine+"/external-task/"+self.task_id+"/complete"
            headers = {"Content-type": "application/json"}
            payload = {
            "workerId" : self.worker_id,
            "variables" : {
            self.variable : {"value" : self.value, "type": "String"},
            "Task report" : {"value" : robot_results_url, "type": "String"}}
            }
            r = requests.post(url, json=payload, headers=headers, verify=False)
            r.raise_for_status()
            logger.warn(f"{self.task_id} completed!")
        except Exception as e:
            logger.error(f"Could not send complete task to engine: {e}")

    def _fail_task(self):
        """
        Sends task failed to engine
        """
        try:
            error_message = str(self.test_message)
            url = self.engine+"/external-task/"+self.task_id+"/failure"
            headers = {"Content-type": "application/json"}
            payload = {
            "workerId" : self.worker_id,
            "errorMessage" : error_message,
            "retries" : 2,
            "retryTimeout": 60000
            }
            r = requests.post(url, json=payload, headers=headers, verify=False)
            r.raise_for_status()
            logger.error(f"{self.task_id} fail: {error_message}")
        except Exception as e:
            logger.error(f"Could not send fail task to engine: {e}")

    def _set_task_completed_variables(self):
        self.result_set = BuiltIn().get_variable_value("${RETURN}")
        for k, v in self.result_set.items():
            self.variable = k
            self.value = v

    def _get_process_id(self):
        try:
            r = requests.get(url = self.engine+"/external-task/"+self.task_id)
            r.raise_for_status()
            if r.json()["processInstanceId"]:
                return r.json()["processInstanceId"]
            else:
                raise NotFound(f"Process id not found")
        except Exception as e:
            logger.error(f"Could not get process id: {e}")

    def _upload_results(self):
        try:
            #TODO: compine results from diferent folders
            time.sleep(random.randint(1, 5))
            process_id = self._get_process_id()
            try:
                self.oc_client.list(process_id+"/")
                self.oc_client.get_file(process_id+"/output.xml","o.xml")
                rebot("o.xml", self.output_file, merge=True, rpa=True, doc=f"Task results for process instance {process_id}",
                    reporttitle=f"{process_id} Task Report", name=".", report=self.report_file, output=self.output_file, log=self.log_file)
            except Exception as e:
                if str(e) == "HTTP error: 404":
                    self.oc_client.mkdir(process_id)
                    pass
                else:
                    raise Exception(f"Error:{e}")
            self.oc_client.put_file(process_id+"/log.html", self.log_file)
            self.oc_client.put_file(process_id+"/output.xml", self.output_file)
            self.oc_client.put_file(process_id+"/report.html", self.report_file)
        except Exception as e:
            logger.error(f"Could not upload results: {e}")
        return self.oc_client.share_file_with_link(process_id).get_link()