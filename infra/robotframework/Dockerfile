FROM python:3-alpine
RUN set -xe && \
    apk upgrade --no-cache && \
    apk add --no-cache \
        nodejs && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rfbrowser init
