#!/usr/bin/env python

from jsonrpclib import Server
import optparse

#
# User, passwords and method to connect to eAPI on switches
#
EAPI_USERNAME = 'admin'
EAPI_PASSWORD = ''
EAPI_ENABLE_PASSWORD = ''
EAPI_METHOD = 'http'

#
# Define available options on the command line to findmac.py
#
usage = 'usage: %prog [options]'
op = optparse.OptionParser(usage=usage)
op.add_option( '-i', '--deviceips', dest='hosts', action='store', help='list of host IP addresses, where to seek check LAG packet path', type='string')
op.add_option( '-s', '--srcmac', dest='srcmac', action='store', help='Src MAC for packet to trace', type='string')
op.add_option( '-d', '--dstmac', dest='dstmac', action='store', help='Dst MAC for packet to trace', type='string')
op.add_option( '-e', '--ethertype', dest='ethertype', action='store', help='Ether type for packet to trace', type='string')
op.add_option( '-p', '--ingressport', dest='ingressport', action='store', help='Ingress port for packet to trace', type='string')
op.add_option( '-v', '--vlanid', dest='vlanid', action='store', help='VLAN id for packet to trace', type='string')
opts, _ = op.parse_args()

#
# Get data from command line
#

hosts = opts.hosts
srcmac = opts.srcmac
dstmac = opts.dstmac
ethertype = opts.ethertype
ingressport = opts.ingressport
vlanid = opts.vlanid
firstrun = 1

#
# Creat a list of IPs from variable hosts
#

iplist = hosts.split()

#
# Trace packet in every switch and print resulsts to STDOUT
#

for ip in iplist:
	switch = Server( '%s://%s:%s@%s/command-api' % ( EAPI_METHOD, EAPI_USERNAME, EAPI_PASSWORD, ip ) )

	response = switch.runCmds(1, ["enable", "show mac address-table address " + dstmac])
	maclist = response[1]["unicastTable"]["tableEntries"]
	for mac in maclist:
		if mac["macAddress"] == dstmac:
			interface = mac["interface"]

	response = switch.runCmds(1, ["enable", "show hostname", "show load-balance destination port-channel " + interface + " src-mac "+ srcmac + " dst-mac " + dstmac + " eth-type " + ethertype + " ingress-interface " + ingressport + " vlan " + vlanid])
	hostname = response[1]["hostname"]
	egressinterface = response[2]["outputIntf"]
	
	print "Hostname: %s" % ( hostname )
	print "Port Channel: %s" % ( interface )
	print "Egress Port channel member: %s" % ( egressinterface )

	response = switch.runCmds(1, ["enable", "show lldp neighbors"])
	neighborlist = response[1]["lldpNeighbors"]
	for neighbor in neighborlist:
		if neighbor["port"] == egressinterface:
			ingressport = neighbor["neighborPort"]
