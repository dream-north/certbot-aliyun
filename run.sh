#!/bin/bash

./certonly.sh

while true; do
    echo "Executing renew at $(date)"
    ./renew.sh
    sleep $RENEW_PERIOD
done
