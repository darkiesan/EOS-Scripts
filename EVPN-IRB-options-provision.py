#!/usr/bin/python

from jsonrpclib import Server
import optparse

USER = "becs"
PASS = "becs"
METHOD = "http"

usage = 'usage: %prog [options]'
op = optparse.OptionParser(usage=usage)
op.add_option( '-t', '--tenant', dest='tenant', action='store', help='Tentant for EVPN and routing', type='string')
op.add_option( '-v', '--vlan', dest='vlan', action='store', help='VLAN for VNI and MAC VRF', type='string')
op.add_option( '-i', '--iplist', dest='iplist', action='store', help='List of IP addresses of switches', type='string')
op.add_option( '-r', '--routing-vni', dest='routingvni', action='store', help='VNI for IP VRF when doing IRB', type='string')
op.add_option( '-x', '--ip-address', dest='ipaddress', action='store', help='IP address for IRB/SVI if applicable', type='string', default="0.0.0.0")
op.add_option( '-n', '--interface', dest='interface', action='store', help='Interface for customer', type='string')
op.add_option( '-y', '--trunk', dest='trunk', action='store', help='Is interface trunk or access', type='string')
op.add_option( '-o', '--irb-option', dest='irb', action='store', help='Use symmetric or asymmetric IRB model', type='string')
opts, _ = op.parse_args()

tenant = opts.tenant
vlan = opts.vlan
vxlan = str(int(vlan) + 10000)

ipstrlist = opts.iplist
iplist = ipstrlist.split()

routingvni = opts.routingvni

if opts.ipaddress != "0.0.0.0":
 ipaddress = opts.ipaddress

interface = opts.interface
trunk = opts.trunk
irboption = opts.irb

for ip in iplist:
 myswitch = Server( '%s://%s:%s@%s/command-api' % ( METHOD, USER, PASS, ip ) )

# Create IP VRF and acctivate routing
 response = myswitch.runCmds(1, ["configure", "vrf definition "+tenant, "ip routing vrf "+tenant] )

# Configure interface vxlan1 with L2 EVPN VNI and IRB VNI 
 response = myswitch.runCmds(1, ["configure", "interface vxlan1", "vxlan vlan "+vlan+" vni "+vxlan, "vxlan vrf "+tenant+" vni "+routingvni] )

# Configure customer access port
 if trunk == "yes":
  response = myswitch.runCmds(1, ["configure", "interface "+interface, "switchport mode trunk", "switchport trunk allowed vlan add "+vlan] )
 else:
  response = myswitch.runCmds(1, ["configure", "interface "+interface, "switchport mode access", "switchport access vlan "+vlan] )

# Create VLAN and SVI if needed
 response = myswitch.runCmds(1, ["configure", "vlan "+vlan] )
 if opts.ipaddress != "0.0.0.0":
  response = myswitch.runCmds(1, ["configure", "interface vlan"+vlan, "description "+tenant, "vrf forwarding "+tenant, "ip address virtual "+ipaddress, ] )
  
# Create MAC VRF and IP VRF in BGP
 result = myswitch.runCmds(1, ["enable", "show ip bgp summary"] )
 asn = result[1]['vrfs']['default']['asn']

 result = myswitch.runCmds(1, ["enable", "show interfaces Loopback0"] )
 router_ip = result[1]['interfaces']['Loopback0']['interfaceAddress'][0]['primaryIp']['address']

 response = myswitch.runCmds(1, ["configure", "router bgp "+str(asn), "vlan "+vlan, "rd "+router_ip+":"+vlan, "route-target both "+vlan+":"+vlan, "redistribute learned"] )
 
 if irboption == "symmetric" and opts.ipaddress != "0.0.0.0": 
  response = myswitch.runCmds(1, ["configure", "router bgp "+str(asn), "vrf "+tenant, "route-target both "+routingvni+":"+routingvni, "redistribute connected" ])
