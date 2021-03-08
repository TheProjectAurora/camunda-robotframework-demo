import robot
import requests
import sys
import time
import docker

class CamundaRFWorker:

    def __init__(self,camunda_url):
        self.camunda_url = camunda_url
        self.camunda_engine_url = self.camunda_url+"/engine-rest"
        self.docker_client = docker.from_env()
        self.poll_interval = 5

    def _start_robot_framework_task(self,topic):
        """
        Starts robot framework container with topic name
        """
        print(f"Starting robot framework task: {topic}")
        try:
            robot_cmd = "robot --pythonpath /tmp --listener /tmp/CamundaListener.py;"+self.camunda_url+" -d /tmp -i "+topic+" -v TOPIC:"+topic+" -v CAMUNDA_HOST:"+self.camunda_url+" /tmp"
            self.docker_client.containers.run("camunda-robotframework-demo_robotframework:latest",network="camunda-robotframework-demo_default",command=robot_cmd)
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
                    self._start_robot_framework_task(t["topicName"])
        except Exception as e:
            print(f"Could not fetch external tasks: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 1:
        t = CamundaRFWorker(sys.argv[1])
        while True:
            t.fetch_robot_framework_tasks_from_engine()
            time.sleep(t.poll_interval)
    else:
        sys.exit("Camunda url missing")