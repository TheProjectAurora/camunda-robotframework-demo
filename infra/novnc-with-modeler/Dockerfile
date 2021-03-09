FROM dorowu/ubuntu-desktop-lxde-vnc:focal

###########################################################################
# NoVNC Setup + Microsoft Visual Studio Code installation with plugins
ENV DEBIAN_FRONTEND=noninteractive DONT_PROMPT_WSL_INSTALL=true
RUN set -xe \
    && wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg \
    && install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/ \
    && sh -c 'echo "deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list' \
    && apt -qq update && apt dist-upgrade -y \
    && apt install -qq --no-install-recommends --allow-unauthenticated -y \
      git \ 
      code \
      npm  \
      unzip \
      nano \
    && apt clean && rm -rf /var/lib/apt/lists/* 
# GENERATE SSL CERT
COPY novnc_openssl.cnf /etc/nginx/ssl/novnc_openssl.cnf
RUN set -xe \
    && openssl req -x509 -config /etc/nginx/ssl/novnc_openssl.cnf -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt
EXPOSE 443
# ADD coder USER
# SOURCE: https://github.com/eficode-academy/code-server/blob/master/docker-images/Dockerfile
# Set password and other coder user things are handled with noVNC environment parameters in docker-compose.yaml
RUN set -xe \
    && adduser --gecos '' --disabled-password coder \
    && set -xe  && usermod -a -G sudo coder
USER coder
ENV HOME=/home/coder
WORKDIR /home/coder
# TODO: Create loop that install extensions
RUN set -xe && \
    code --verbose --log debug --install-extension redhat.vscode-yaml
#TODO: NoVNC binary should be executed under root, under coder it not work
USER root

###########################################################################
# TOOLING
#####
# INSTALL: https://camunda.com/download/modeler/
RUN set -xe \
    && apt -qq update \
    && apt install -qq --no-install-recommends --allow-unauthenticated -y \
      python3 \
      python3-pip \
      docker.io \
    && apt clean && rm -rf /var/lib/apt/lists/* \
    && cd / \
    && wget -O camunda-modeler-linux-x64.tar.gz https://downloads.camunda.cloud/release/camunda-modeler/4.6.0/camunda-modeler-4.6.0-linux-x64.tar.gz \
    && tar -zxvf camunda-modeler-linux-x64.tar.gz \
    && rm -Rfv camunda-modeler-linux-x64.tar.gz \
    && chmod -v +x camunda-modeler-*-linux-x64/camunda-modeler \
    && ln -sv `echo $(pwd)/$(ls -h camunda-modeler-*-linux-x64/camunda-modeler)` /usr/bin/camunda-modeler \
    && cd camunda-modeler-*-linux-x64/resources/plugins \
    && git clone https://github.com/datakurre/camunda-modeler-robot-plugin
