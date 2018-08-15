#!/usr/bin/env python

from jsonrpclib import Server
import optparse

USER = "arista"
PASS = "arista"
METHOD = "http"

usage = 'usage: %prog [options]'
op = optparse.OptionParser(usage=usage)
op.add_option( '-v', '--vlan', dest='vlan', action='store', help='VLAN for VNI and MAC VRF', type='string')
op.add_option( '-i', '--iplist', dest='iplist', action='store', help='List of IP addresses of switches', type='string')

opts, _ = op.parse_args()

vlan = opts.vlan
vxlan = str(int(vlan) + 10000)

ipstrlist = opts.iplist
iplist = ipstrlist.split()

for ip in iplist:

# Login to each switch in the ip list
 myswitch = Server( '%s://%s:%s@%s/command-api' % ( METHOD, USER, PASS, ip ) )

# Create VLAN 
 response = myswitch.runCmds(1, ["configure", "vlan "+vlan] )

# Configure interface vxlan1 with VNI for the VLAN
 response = myswitch.runCmds(1, ["configure", "interface vxlan1", "vxlan vlan "+vlan+" vni "+vxlan, "vxlan vrf "+tenant+" vni "+routingvni] )
