FROM camunda/camunda-bpm-platform
# TRY TO GET https://github.com/datakurre/camunda-cockpit-plugins/ working.
# WITH: docker run -d -P camunda-robotframework-demo_camunda
# WORKING OTHER WAYS NOT WORK
USER root
RUN set -xe && \
    apk upgrade --no-cache && \
    apk add --no-cache \
        git
USER camunda
# https://github.com/datakurre/camunda-cockpit-plugins/ OR https://datakurre.pandala.org/2021/01/camunda-cockpit-history-plugin/ installation
RUN wget -P /camunda/webapps/camunda/app/cockpit/scripts/ https://raw.githubusercontent.com/datakurre/camunda-cockpit-plugins/master/definition-historic-activities.js && \
    wget -P /camunda/webapps/camunda/app/cockpit/scripts/ https://raw.githubusercontent.com/datakurre/camunda-cockpit-plugins/master/instance-historic-activities.js && \
    wget -P /camunda/webapps/camunda/app/cockpit/scripts/ https://raw.githubusercontent.com/datakurre/camunda-cockpit-plugins/master/instance-route-history.js
COPY --chown=camunda:camunda cockpit/config.js /camunda/webapps/camunda/app/cockpit/scripts/.
