=================
EVPN-provision.py
=================

This script is intended as a base L2 EVPN provisioning template.
It assumes symmetric routing and when two switches are chosen to
be the symmetric routers, that they run vARP. When using the script
for the vARP routers, specify -x prefix/len ex. -x 20.0.0.1/24.
On switches that will not be chosen as routers, use -x 0.0.0.0 and
IP configuration on SVIs will be skipped.

The -i switch specifies a list of switches to iterate the script on.
Make sure that all IPs/switches are either NON-routers or are ROUTERS
(meant to do the symmetric routing). Ex. -i "192.168.100.102 192.168.100.103"
Even if only one switch is to be configured, the format need to be -i "x.y.w.z".
Ex. -i "192.168.100.101"

Pls read script to make sure all command line options are supplied to the script when executed.

==========================
EVPN-IRB-options-provision
==========================

This script is intended as a base L2 EVPN provisioning template.
It uses everything mentioned above for EVPN-provisioning.oy, but also makes it possible to
specify asymmetric routing. This means when -o asymmetric is specified,
-x x.y.w.z to specify SVI vARP address also must be specified or the script fails.
Ex. -o asymmetric -x 20.0.0.1/24

Pls read script to make sure all command line options are supplied to the script when executed.

========
HashTest
========

This script is intended to statistically test the hashing for LAG groups in DANZ scenarios.
It requires the python library scapy and should be executed on a script host connected to a
single port on the a Tap Agg switch. The script sends packets and records the exit interface
(being member in a LAG group) in a SQLITE file so that reports can be made afterwards to
investigate the statistica outfall.

===============
find_counter.py
===============

Find and print packet coubter for an interface.

==========
findmac.py
==========

This script is intended to find a mac address supplied via command line option in switches
in a list supplied via command line option. The script will print hostname of the switch
and on which ports the mac address was found.

==========
rand_no.py
==========

Generate random number.

==============
send_packet.py
==============

Scapy example on howto send a packet.

=============
RouteTrack.sh
=============

Example of an onboard script checking connectivity and based on the result performs config
actions on the switch.

============
ipaddress.py
============

eAPI exampel script for setting IP address on interfaces using onboard scripting or remote
script host. The script takes as arguments IP to connect to, IP/Netmask to add and interface to
add IP to.
