FROM python:3-alpine
COPY ./config/CamundaGMAILWorker.py /app/CamundaGMAILWorker.py
COPY ./requirements.txt /tmp/requirements.txt
RUN set -xe && \
    chmod +x /app/CamundaGMAILWorker.py && \
    pip3 install install -r /tmp/requirements.txt
