#!/bin/bash

HOSTUP=Y
PingInterval=2
FailureCount=3
Count=0
while true; do

for i in 192.168.123.4
do
ping -c 1 -W 1 $i &> /dev/null
PingResult=$?

if [ $PingResult = "1" ]; then
let "Count++"
if [ "$HOSTUP" = "Y" ]; then
if [ $Count = "$FailureCount" ]; then
NOW=`date`
echo "Host is down at" $NOW >> /mnt/flash/RouteTrack.log
FastCli -p15 -c '
enable
conf term
no ip route 10.0.0.0/24 192.168.123.4'
HOSTUP=N
fi
else
HOSTUP=N
fi
fi

if [ $PingResult = "0" ]; then
if [ "$HOSTUP" = "N" ]; then
NOW=`date`
echo "Host is up at" $NOW >> /mnt/flash/RouteTrack.log
Count=0
FastCli -p15 -c '
enable
conf term
ip route 10.0.0.0/24 192.168.123.4'
HOSTUP=Y
else
HOSTUP=Y
fi
fi
done

sleep $PingInterval
done

