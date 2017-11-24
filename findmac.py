#!/usr/bin/python

from jsonrpclib import Server
import optparse
import signal
import copy

#
# USer, passwords and method to connect to eAPI on switches
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
op.add_option( '-i', '--ip', dest='hosts', action='store', help='list of host IP addresses, where to seek mac addresses', type='string')
op.add_option( '-m', '--mac', dest='mac', action='store', help='MAC address which will be searched for', type='string')
opts, _ = op.parse_args()

#
# Create a list with IPs from the command line option "-i, --ip"
#
hosts = opts.hosts
iplist = hosts.split()

#
# Collect the MAC address being searched in the network
#
mac = opts.mac

#
# Itereate through the iplist, i.e. iterate through switches
# and collect hostname. If MAC address is found on switch print
# the MAC address and what interface where it was seen
#
for ip in iplist :

 switch = Server( '%s://%s:%s@%s/command-api' % ( EAPI_METHOD, EAPI_USERNAME, EAPI_PASSWORD, ip ) )
 response = switch.runCmds(1, ["show hostname", "show mac address-table address "+mac])


 hostname = response[0]["hostname"]
 macs = response[1]["unicastTable"]["tableEntries"]

 print '\n'
 print hostname 
 print '--------'


 for element in macs :
  print '{}: {}'.format(element["interface"], element["macAddress"])

