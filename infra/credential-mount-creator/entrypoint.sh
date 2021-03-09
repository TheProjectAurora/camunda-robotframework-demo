#!/bin/bash
while [ /bin/true ]
do
    rm -rf $2
    cp -rfv $1/* $2/.
    chmod -Rv 777 $2/*
    content1=$(ls -1 $1)
    content2=$(ls -1 $1)
    if [ "$content1" == "$content2" ]; then
        break;
    fi
done