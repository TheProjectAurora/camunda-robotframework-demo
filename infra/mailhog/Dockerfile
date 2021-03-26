FROM mailhog/mailhog
USER root
COPY send /bin/send
RUN set -xe && \
    wget https://github.com/mailhog/mhsendmail/releases/download/v0.2.0/mhsendmail_linux_amd64 && \
    chmod +x mhsendmail_linux_amd64 /bin/send && \
    mv mhsendmail_linux_amd64 /bin/mhsendmail
USER mailhog
