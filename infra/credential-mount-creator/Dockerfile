FROM alpine:3.12  
COPY entrypoint.sh /
RUN set -xe && \
    apk upgrade --no-cache && \
    apk add --no-cache \
        bash && \
    chmod +x /entrypoint.sh
