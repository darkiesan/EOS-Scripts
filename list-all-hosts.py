#!/usr/bin/python

from jsonrpclib import Server
import optparse
import signal
import copy

#
# User, passwords and method to connect to eAPI on switches
#
EAPI_USERNAME = 'cvpadmin'
EAPI_PASSWORD = 'pzkpw51B'
EAPI_ENABLE_PASSWORD = ''
EAPI_METHOD = 'http'

#
# Define available options on the command line to findmac.py
#
usage = 'usage: %prog [options]'
op = optparse.OptionParser(usage=usage)
op.add_option( '-i', '--ip', dest='hosts', action='store', help='list of host or IP addresses to find hosts to list', type='string')
op.add_option( '-v', '--vrf', dest='vrf', action='store', help='Select vrf to search IP info in, if not specified the global table is searched', type='string', default="default")
opts, _ = op.parse_args()

#
# Create a list with IPs from the command line option "-i, --ip"
#

hosts = opts.hosts
iplist = hosts.split()
vrf = opts.vrf

#
# Itereate through the iplist, i.e. iterate through switches
# and collect hosts and print
#

for ip in iplist:

	switch = Server( '%s://%s:%s@%s/command-api' % ( EAPI_METHOD, EAPI_USERNAME, EAPI_PASSWORD, ip ) )
	if vrf == "default":
		response = switch.runCmds(1, ["show hostname", "show arp"])
	else:
		response = switch.runCmds(1, ["show hostname", "show arp vrf "+vrf])

	hostname = response[0]["hostname"]
	arps = response[1]["ipV4Neighbors"]

	print "Switch: %s" % ( hostname )
	print "=================================================================================="

	if arps != []:
		for arp in arps:
			vlanfound = 0
			mac_address = arp["hwAddress"]
			host_ip = arp["address"]
			interface_list = arp["interface"].split(',')
			for interface in interface_list:
				if "Vlan" in interface:
					vlan = interface
					vlanfound = 1
				else:
					port = interface

			if "Vxlan1" in interface:
				print ""
			else:
				if vrf == "default" and vlanfound == 1:
					print "IP: %s, MAC: %s, Vlan: %s, Port: %s" % ( host_ip , mac_address , vlan , interface )
				if vrf != "default" and vlanfound == 1:
					print "VRF: %s, IP: %s, MAC: %s, Vlan: %s, Port: %s" % ( vrf, host_ip , mac_address , vlan , interface )
				if vrf == "default" and vlanfound == 0:
					print "IP: %s, MAC: %s, Vlan: N/A routed port, Port: %s" % ( host_ip , mac_address , interface )
				if vrf != "default" and vlanfound == 0:
					print "VRF: %s, IP: %s, MAC: %s, Vlan: N/A routed port, Port: %s" % ( vrf, host_ip , mac_address , interface )
				print ""