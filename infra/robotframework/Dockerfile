FROM marketsquare/robotframework-browser
COPY requirements.txt /tmp/requirements.txt
ENV PYTHONPATH=/home/pwuser/.local/lib/python3.8/site-packages
RUN set -xe && \
    pip3 install --no-cache-dir -r /tmp/requirements.txt
USER root
RUN apt -qq update -y \
    && apt install -qq --no-install-recommends --allow-unauthenticated -y \
    git
USER pwuser