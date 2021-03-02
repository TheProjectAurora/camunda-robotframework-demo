FROM python:3-alpine
COPY ./config/CamundaRFWorker.py /app/CamundaRFWorker.py
COPY ./requirements.txt /tmp/requirements.txt
RUN set -xe && \
    chmod +x /app/CamundaRFWorker.py && \
    pip3 install install -r /tmp/requirements.txt