FROM marketsquare/robotframework-browser
COPY requirements.txt /tmp/requirements.txt
COPY Tasks/CamundaDemoTasks.robot /tmp/CamundaDemoTasks.robot
RUN set -xe && \
    pip3 install --no-cache-dir -r /tmp/requirements.txt
