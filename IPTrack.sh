#!/bin/bash

HOSTUP=Y
PingInterval=2
FailureCount=3
Count=0
while true; do

for i in CHANGE_TO_MONITORED_IP
do
ping -c 1 -W 1 $i &> /dev/null
PingResult=$?

if [ $PingResult = "1" ]; then
let "Count++"
if [ "$HOSTUP" = "Y" ]; then
if [ $Count = "$FailureCount" ]; then
NOW=`date`
echo "Host CHANGE_TO_MONITORED_IP is down at" $NOW >> /mnt/flash/IPTrack.log
FastCli -p15 -c '
INSERT
YOUR
EOS
COMMANDS
HERE
'
HOSTUP=N
fi
else
HOSTUP=N
fi
fi

if [ $PingResult = "0" ]; then
if [ "$HOSTUP" = "N" ]; then
NOW=`date`
echo "Host CHANGE_TO_MONITORED_IP is up at" $NOW >> /mnt/flash/IPTrack.log
Count=0
FastCli -p15 -c '
INSERT
YOUR
EOS
COMMANDS
HERE
'
HOSTUP=Y
else
HOSTUP=Y
fi
fi
done

sleep $PingInterval
done

