#!/usr/bin/env bash

set -x
echo "copy our preset config"
cp -v /tmp/cruise-config.xml /godata/config/cruise-config.xml
chown -v go:root /godata/config/cruise-config.xml
GATEWAY=$(hostname -i | sed 's|\(^[0-9]*\.[0-9]*\.[0-9]*\.\)[0-9]*|\11|g')
echo "INFO: Change elastic agents configuration GOCD_SERVER_ADDRESS=${GATEWAY}"
sed -i "s|GOCD_SERVER_ADDRESS|${GATEWAY}|g" /godata/config/cruise-config.xml
#SET GIT REPO
sed -i "s|GITREPO|${GITREPO}|g" /godata/config/cruise-config.xml
sed -i "s|GITBRANCH|${GITBRANCH}|g" /godata/config/cruise-config.xml