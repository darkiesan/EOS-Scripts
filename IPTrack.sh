############################################################################
#									   #
# To use the script, uplaod it to an EOS device, place it in /mnt/flash.   #
# In the script, change CHANGE_TO_MONITORED_IP to the IP address that will #
# be tracked and monitored. Go to the FastCli command for ping success     #
# and failure and replace:						   #
# INSERT								   #
# YOUR									   #
# EOS									   #
# COMMAND								   #
# HERE									   #
#									   #
# with the approriate actions you want the script to do.		   #
#									   #
# Then start BASH on the EOS device and run: touch /mnt/flash/IPTrack.log  #
# 									   #
# Add following config via EOS CLI:					   #
# daemon IPTrack							   #
#    exec /mnt/flash/IPTrack.sh						   #
#    no shutdown							   #
#									   #
# Now it is running!							   #
############################################################################

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

