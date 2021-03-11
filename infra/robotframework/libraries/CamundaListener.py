import requests
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import owncloud
import os

"""Camunda listener takes care of task status update to engine
"""
class CamundaListener:
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, camunda_url):
        self.camunda_url = camunda_url
        self.camunda_engine_rest_url = self.camunda_url+"/engine-rest"
        self.task_id = None
        self.worker_id = None
        self.test_message = None
        self.result_set = []
        self.oc_client = owncloud.Client("http://owncloud:8080")

    def end_test(self, data, result):
        try:
            self.task_id = BuiltIn().get_variable_value("${TASK_ID}")
            self.worker_id = BuiltIn().get_variable_value("${WORKER_ID}")
            self.test_message = BuiltIn().get_variable_value("${TEST_MESSAGE}")
            if result.passed:
                self._set_task_completed_variables()
                self._complete_task()
            else:
                self._fail_task(self.test_message)
        except Exception as e:
            logger.error(f"Error when updating task results: {e}")

    def report_file(self, path):
        self._upload_results_to_cloud(path)

    def _complete_task(self):
        """
        Sends task complete to engine
        """
        try:
            url = self.camunda_engine_rest_url+"/external-task/"+self.task_id+"/complete"
            headers = {"Content-type": "application/json"}
            payload = {
            "workerId" : self.worker_id,
            "variables" : {
            self.variable : {"value" : self.value, "type": "String"}}
            }
            r = requests.post(url, json=payload, headers=headers, verify=False)
            r.raise_for_status()
            logger.warn(f"Task {self.task_id} completed!")
        except Exception as e:
            logger.error(f"Could not send complete task to engine: {e}")

    def _fail_task(self,error_message):
        """
        Sends task failed to engine
        """
        try:
            error_message = str(error_message)
            url = self.camunda_engine_rest_url+"/external-task/"+self.task_id+"/failure"
            headers = {"Content-type": "application/json"}
            payload = {
            "workerId" : self.worker_id,
            "errorMessage" : error_message,
            "retries" : 2,
            "retryTimeout": 60000
            }
            r = requests.post(url, json=payload, headers=headers, verify=False)
            r.raise_for_status()
            logger.error(f"Task {self.task_id} failed! Error message:{error_message}")
        except Exception as e:
            logger.error(f"Could not send fail task to engine: {e}")

    def _set_task_completed_variables(self):
        self.result_set = BuiltIn().get_variable_value("${RETURN}")
        for k, v in self.result_set.items():
            self.variable = k
            self.value = v

    def _upload_results_to_cloud(self,path):
        try:
            dir = os.getcwd()
            logger.error(f"PATH: {path}")
            logger.error(f"cur dir: {dir}")
            self.oc_client.login("sakke","sakke")
            self.oc_client.put_file(f"{path}","report.html")
            link_info = self.oc_client.share_file_with_link("report.html")
            print(f"Report file uploaded:{link_info}")
        except Exception as e:
            print(f"Could not upload report file: {e}")
            logger.error(f"Could not upload report file: {e}")
