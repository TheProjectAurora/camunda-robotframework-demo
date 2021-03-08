FROM python:3-alpine
RUN mkdir -p /app
COPY ./libraries /app/libraries
COPY ./CamundaGMAILWorker.py /app
COPY ./requirements.txt /tmp
RUN set -xe && \
    chmod +x /app/CamundaGMAILWorker.py && \
    pip3 install install -r /tmp/requirements.txt
