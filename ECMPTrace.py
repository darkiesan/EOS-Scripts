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
op.add_option( '-s', '--srcip', dest='srcip', action='store', help='Src IP for packet to trace', type='string')
op.add_option( '-d', '--dstmac', dest='dstip', action='store', help='Dst IP for packet to trace', type='string')
op.add_option( '-e', '--protocol', dest='protocol', action='store', help='IP protocol packet to trace, i.e. 4 for IPv4, 6 for TCP, 17 for UDP etc', type='string')
op.add_option( '-p', '--ingressport', dest='ingressport', action='store', help='Ingress port for packet to trace', type='string')
opts, _ = op.parse_args()

#
# Get data from command line
#

hosts = opts.hosts
srcip = opts.srcip
dstip = opts.dstip
protocol = opts.protocol
ingressport = opts.ingressport

#
# Creat a list of IPs from variable hosts
#

iplist = hosts.split()

#
# Trace packet in every switch and print resulsts to STDOUT
#

for ip in iplist:
	switch = Server( '%s://%s:%s@%s/command-api' % ( EAPI_METHOD, EAPI_USERNAME, EAPI_PASSWORD, ip ) )

	response = switch.runCmds(1, ["enable", "show hostname", "show load-balance destination ip ingress-interface " + ingressport + " src-ipv4-address "+ srcip + " dst-ipv4-address " + dstip + " ip-protocol " + protocol])
	hostname = response[1]["hostname"]
	egressinterface = response[2]["outputIntf"]
	
	print "Hostname: %s" % ( hostname )
	print "Egress Port channel member: %s" % ( egressinterface )

	response = switch.runCmds(1, ["enable", "show lldp neighbors"])
	neighborlist = response[1]["lldpNeighbors"]
	for neighbor in neighborlist:
		if neighbor["port"] == egressinterface:
			ingressport = neighbor["neighborPort"]
