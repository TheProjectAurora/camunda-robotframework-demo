import requests
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import owncloud
import os

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
        self.oc_client = owncloud.Client("http://owncloud:8080")

    def end_test(self, data, result):
        try:
            self.task_id = BuiltIn().get_variable_value("${TASK_ID}")
            self.worker_id = BuiltIn().get_variable_value("${WORKER_ID}")
            test_message = BuiltIn().get_variable_value("${TEST_MESSAGE}")
            if result.passed:
                self._set_task_completed_variables()
                self._complete_task()
            else:
                self._fail_task(test_message)
        except Exception as e:
            logger.error(f"Error when end test happened: {e}")

    def close(self, path):
        try:
            self._upload_results()
        except Exception as e:
            logger.error(f"Error when close happened: {e}")

    def _complete_task(self):
        """
        Sends task complete to engine
        """
        try:
            url = self.engine+"/external-task/"+self.task_id+"/complete"
            headers = {"Content-type": "application/json"}
            payload = {
            "workerId" : self.worker_id,
            "variables" : {
            self.variable : {"value" : self.value, "type": "String"}}
            }
            r = requests.post(url, json=payload, headers=headers, verify=False)
            r.raise_for_status()
            logger.warn(f"{self.task_id} completed!")
        except Exception as e:
            logger.error(f"Could not send complete task to engine: {e}")

    def _fail_task(self,error_message):
        """
        Sends task failed to engine
        """
        try:
            error_message = str(error_message)
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
            r = requests.get(url = self.engine+"/external-task/"self.task_id)
            r.raise_for_status()
            for t in r.json():
                if t["processInstanceId"]:
                    return t["processInstanceId"]
            else:
                raise NotFound(f"Process id not found")
        except Exception as e:
            logger.error(f"Could not get process id: {e}")

    def _upload_results(self):
    try:
        process_id = self._get_process_id()
        try:
            self.oc_client.list(process_id+"/")
            self.oc_client.get_file(process_id+"/output.xml","o.xml")
            rebot("o.xml", "/output.xml", report="report.html", output="output.xml", log="log.html")
        except Exception as e:
            if str(e) == "HTTP error: 404":
                self.oc_client.mkdir(process_id)
                pass
            else:
                raise Exception(f"Error:{e}")
        self.oc_client.put_file(process_id+"/log.html", "log.html")
        self.oc_client.put_file(process_id+"/output.xml", +"output.xml")
        self.oc_client.put_file(process_id+"/report.html", +"report.html")
    except Exception as e:
        logger.error(f"Could not send fail task to engine: {e}")
    return self.oc_client.share_file_with_link(process_id)