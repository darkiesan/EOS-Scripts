#!/usr/bin/env python
#
# management api http-commands
#   protocol unix-socket
#
# event-handler InterfaceTrack
#   trigger on-intf Ethernet1 operstatus
#   action bash /mnt/flash/InterfaceTrack.py
#
# ONE EVENT HANDLER PER INTERFACE TO MONITOR. THEY CAN ALL CALL SAME SCRIPT.
#
# PLEASE NOTE YOU NEED TO MANUALLY CHANGE MONITORED INTERFACES BELOW AND ALSO
# CHANGE INTERFACE THAT WILL BE ALTERED IF THE EVENT IS TRIGGERED.
#

from jsonrpclib import Server

#
# Check status of monitored interfaces when the on-intf event is triggered.
#

switch = Server( "unix:/var/run/command-api.sock")
result = switch.runCmds(1, ["show interfaces Ethernet1", "show interfaces Ethernet2"])

#
#  Check if all interfaces are up. If they are all down, shut interface/interfaces towards servers.
#  If at least one is up, activate server interfaces again.
#

if result[0]['interfaces']['Ethernet1']['interfaceStatus'] != "connected" and result[1]['interfaces']['Ethernet2']['interfaceStatus'] != "connected":
	switch.runCmds(1, ["enable", "configure", "interface Ethernet3", "shutdown"])
else:
	switch.runCmds(1, ["enable", "configure", "interface Ethernet3", "no shutdown"])
