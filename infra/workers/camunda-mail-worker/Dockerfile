FROM python:3-alpine
RUN mkdir -p /app
COPY ./CamundaMAILWorker.py /app
COPY ./requirements.txt /tmp
RUN set -xe && \
    chmod +x /app/CamundaMAILWorker.py && \
    pip3 install install -r /tmp/requirements.txt
