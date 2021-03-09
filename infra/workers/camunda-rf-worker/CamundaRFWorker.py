import requests
import sys
import time
import docker

class CamundaRFWorker:

    def __init__(self,camunda_url,poll_interval=5):
        self.camunda_url = camunda_url
        self.camunda_engine_url = self.camunda_url+"/engine-rest"
        self.docker_client = docker.from_env()
        self.robot_container = "camunda-robotframework-demo_robotframework:latest"
        self.container_network = "camunda-robotframework-demo_default"
        self.robot_listener = "CamundaListener.py"
        self.creds_volume_mount = ["camunda-robotframework-demo_credentials:/credentials"]
        self.git_repo_param_name = "git_repo"
        self.poll_interval = poll_interval

    def _start_robot_framework_task(self,topic,task_id):
        """
        Starts robot framework container with topic name
        """
        try:
            print(f"Starting robot framework task: {topic}")
            git_repo = self._fetch_git_repository_for_task(task_id)
            print(task_id+"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"+str(git_repo))
            robot_cmd = f"robot --pythonpath /tmp --listener /tmp/{self.robot_listener};{self.camunda_url} -d /tmp -i {topic} -v TOPIC:{topic} -v CAMUNDA_HOST:{self.camunda_url} /tmp"
            self.docker_client.containers.run(self.robot_container, network=self.container_network, volumes=self.creds_volume_mount, command=robot_cmd, detach=True, auto_remove=True)
        except Exception as e:
            print(f"Could not complete robot framework task: {e}")

    def fetch_robot_framework_tasks_from_engine(self):
        """
        Polls camunda engine for robot tasks. If robot tasks are found starts rf container.
        """
        try:
            r = requests.get(url = self.camunda_engine_url+"/external-task")
            r.raise_for_status()
            task_count = len(r.json())
            print(f"{task_count} external task(s) found from engine")
            for t in r.json():
                if "robot" in t["activityId"] and (not t["workerId"] and not t["retries"]):
                    self._start_robot_framework_task(t["topicName"],t["id"])
        except Exception as e:
            print(f"Could not fetch external tasks: {e}")

    def _fetch_git_repository_for_task(self,task_id):
        """
        Fetch task git repository. Git repo variable must be set in task output parameters section.
        If variable not found, raises an exception
        """
        try:
            r = requests.get(url = self.camunda_engine_url+"/variable-instance?taskId="+task_id+"&variableName="+self.git_repo_param_name)
            r.raise_for_status()
            print(f"nothing here")
            for t in r.json():
                if t["value"]:
                    return t["value"]
        except Exception as e:
            print(f"Could not fetch git repo variable for task {task_id}: {e}")
        

if __name__ == "__main__":
    if len(sys.argv) != 1:
        t = CamundaRFWorker(sys.argv[1])
        while True:
            t.fetch_robot_framework_tasks_from_engine()
            time.sleep(t.poll_interval)
    else:
        sys.exit("Camunda url missing")