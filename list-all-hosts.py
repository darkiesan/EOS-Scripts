#!/usr/bin/python

from jsonrpclib import Server
import optparse
import signal
import copy

#
# User, passwords and method to connect to eAPI on switches
#
EAPI_USERNAME = 'myuser'
EAPI_PASSWORD = 'mypass'
EAPI_ENABLE_PASSWORD = ''
EAPI_METHOD = 'http'

#
# Define available options on the command line to findmac.py
#
usage = 'usage: %prog [options]'
op = optparse.OptionParser(usage=usage)
op.add_option( '-i', '--ip', dest='hosts', action='store', help='list of host or IP addresses to find hosts to list', type='string')
opts, _ = op.parse_args()

#
# Create a list with IPs from the command line option "-i, --ip"
#

hosts = opts.hosts
iplist = hosts.split()

#
# Itereate through the iplist, i.e. iterate through switches
# and collect hosts and print
#

for ip in iplist:

	switch = Server( '%s://%s:%s@%s/command-api' % ( EAPI_METHOD, EAPI_USERNAME, EAPI_PASSWORD, ip ) )
	response = switch.runCmds(1, ["show hostname", "show mac address-table"])


	hostname = response[0]["hostname"]
	macs = response[1]["unicastTable"]["tableEntries"]

	print "Switch: %s" % ( hostname )
	print "=================================================================================="

	for mac in macs:
		switch = Server( '%s://%s:%s@%s/command-api' % ( EAPI_METHOD, EAPI_USERNAME, EAPI_PASSWORD, ip ) )
		mac_address = mac["macAddress"]
		vlan = mac["vlanId"]
		interface = mac["interface"]

		response = switch.runCmds(1, ["show arp mac-address "+mac_address])
		
		if response[0]["ipV4Neighbors"]["hwAddress"] == mac_address:
			host_ip = response[0]["ipV4Neighbors"]["address"]

		print "IP: %s, MAC: %s, Vlan: %s, Port: %s" % ( host_ip , mac_address , vlan , interface )
