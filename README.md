# camunda-robotframework-demo

- Unix socker privialedges so host docker coulbe utilized from container: ```chmod 777 /var/run/docker.sock```
- By default novnc-camunda-modeler is not started. Execute ```docker-compose scale novnc-with-modeler=1``` to start it.