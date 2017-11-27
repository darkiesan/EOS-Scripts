#!/usr/bin/python

from jsonrpclib import Server
import optparse

USER = "becs"
PASS = "becs"
METHOD = "http"

usage = 'usage: %prog [options]'
op = optparse.OptionParser(usage=usage)
op.add_option( '-t', '--tenant', dest='tenant', action='store', help='Tentant for EVPN and routing', type='string')
op.add_option( '-v', '--vni', dest='vlan', action='store', help='VLAN for VNI and MAC VRF', type='string')
op.add_option( '-i', '--iplist', dest='iplist', action='store', help='List of IP addresses of switches', type='string')
op.add_option( '-a', '--ip-address', dest='ipaddress', action='store', help='IP address for IRB/SVI if applicable', type='string', default="0.0.0.0")
op.add_option( '-n', '--interface', dest='interface', action='store', help='Interface for customer', type='string')
opts, _ = op.parse_args()

tenant = opts.tenant
vni = opts.vni
ipstrlist = opts.iplist
iplist = ipstrlist.split()
ipaddress = opts.ipaddress
interface = opts.interface

for ip in iplist:
 myswitch = Server( '%s://%s:%s@%s/command-api' % ( METHOD, USER, PASS, ip ) )

# Create IP VRF and acctivate routing
 response = myswitch.runCmds(1, ["configure", "vrf definition "+tenant, "ip routing vrf "+tenant] )

# Configure interface vxlan1 with L3 EVPN VNI
 response = myswitch.runCmds(1, ["configure", "interface vxlan1", "vxlan vrf "+tenant+" vni "+vni] )

# Configure CE facing interface
response = myswitch.runCmds(1, ["configure", "interface "+interface, "no switchport", "description "+tenant, "vrf forwarding "+tenant, "ip address "+ipaddress] )
  
# Create MAC VRF and IP VRF in BGP
 result = myswitch.runCmds(1, ["enable", "show ip bgp summary"] )
 asn = result[1]['vrfs']['default']['asn']

 result = myswitch.runCmds(1, ["enable", "show interfaces Loopback0"] )
 router_ip = result[1]['interfaces']['Loopback0']['interfaceAddress'][0]['primaryIp']['address']

 response = myswitch.runCmds(1, ["configure", "router bgp "+str(asn), "vrf "+tenant, "rd "+router_ip":"+vni, "route-target both "+vni+":"+vni, "redistribute connected", "router-id "+router_ip ])
