import requests
import sys
import time
import docker

class NotFound(Exception):
    pass

class CamundaRFWorker:

    def __init__(self,camunda_url,poll_interval=5):
        self.camunda_url = camunda_url
        self.camunda_engine_url = self.camunda_url+"/engine-rest"
        self.docker_client = docker.from_env()
        self.robot_container = "camunda-robotframework-demo_robotframework:latest"
        self.container_network = "camunda-robotframework-demo_default"
        self.robot_listener = "CamundaListener.py"
        self.creds_volume_mount = ["camunda-robotframework-demo_credentials:/credentials"]
        self.git_repo_param = "git_repo"
        self.git_hub_url = "https://github.com/"
        self.poll_interval = poll_interval

    def _start_robot_framework_container(self,topic,task_id):
        """
        Starts robot framework container with topic name
        """
        try:
            print(f"Starting robot framework task: {topic}")
            git_repo = self._fetch_git_repository_for_task(task_id)
            git_clone_cmd = f"git clone {self.git_hub_url}{git_repo}"
            print(git_clone_cmd)
            robot_cmd = f"robot --pythonpath /tmp --pythonpath ./libaries --listener /tmp/{self.robot_listener};{self.camunda_url} -d /tmp -i {topic} -v TOPIC:{topic} -v CAMUNDA_HOST:{self.camunda_url} /tmp"
            print("############")
            run_cmd = f"cd /tmp && {git_clone_cmd} && {robot_cmd}"
            print("############")
            #git clone -b <branchname> <remote-repo-url>
            cmdddd = f"cd /tmp && git clone -b feature/git_clone_before_running_tasks https://github.com/TheProjectAurora/camunda-robotframework-demo && cd /tmp/camunda-robotframework-demo && robot ."
            command2 =["/bin/sh", "-c", cmdddd]
            self.docker_client.containers.run(self.robot_container, network=self.container_network, volumes=self.creds_volume_mount, entrypoint=command2, detach=False, auto_remove=False)
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
                    self._start_robot_framework_container(t["topicName"],t["activityId"])
        except Exception as e:
            print(f"Could not fetch external tasks: {e}")

    def _fetch_git_repository_for_task(self,task_id):
        """
        Fetch task git repository. Git repo variable must be set in task parameters section.
        If variable not found, raises an exception
        """
        try:
            r = requests.get(url = self.camunda_engine_url+"/variable-instance?&variableName="+self.git_repo_param)
            r.raise_for_status()
            for t in r.json():
                if task_id in t["activityInstanceId"]:
                        if t["value"]:
                            git_repo = t["value"]
                            return git_repo
            else:
                raise NotFound(f"Git repository not found")
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