FROM marketsquare/robotframework-browser
COPY requirements.txt /tmp/requirements.txt
COPY Tasks/CamundaDemoTasks.robot /tmp/CamundaDemoTasks.robot
COPY resources/camunda_demo_resource.robot /tmp/camunda_demo_resource.robot
COPY libraries/GmailRFLib.py /tmp/GmailRFLib.py
COPY libraries/CamundaListener.py /tmp/CamundaListener.py
ENV PYTHONPATH=/home/pwuser/.local/lib/python3.8/site-packages
RUN set -xe && \
    pip3 install --no-cache-dir -r /tmp/requirements.txt
