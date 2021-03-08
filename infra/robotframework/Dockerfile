FROM marketsquare/robotframework-browser
COPY requirements.txt /tmp/requirements.txt
COPY Tasks/CamundaDemoTasks.robot /tmp/CamundaDemoTasks.robot
COPY libraries/GmailRFLib.py /tmp/GmailRFLib.py
COPY libraries/CamundaListener.py /tmp/CamundaListener.py
COPY credentials/credentials.json /tmp/credentials/credentials.json
COPY credentials/token.json /tmp/credentials/token.json
ENV PYTHONPATH=/home/pwuser/.local/lib/python3.8/site-packages
RUN set -xe && \
    pip3 install --no-cache-dir -r /tmp/requirements.txt
