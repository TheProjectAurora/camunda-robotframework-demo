FROM python:3-alpine
RUN mkdir -p /app
COPY requirements.txt /tmp/.
RUN set -xe && \
    pip3 install install -r /tmp/requirements.txt
COPY CamundaRFWorker.py /app/.
RUN set -xe && \
    chmod +x /app/CamundaRFWorker.py
