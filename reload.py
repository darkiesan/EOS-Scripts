#!/usr/bin/python

from jsonrpclib import Server
import optparse
import signal
import copy

#
# Define available options on the command line to findmac.py
#
usage = 'usage: %prog [options]'
op = optparse.OptionParser(usage=usage)
op.add_option( '-u', '--user', dest='user', action='store', help='Username to use for switch login', type='string')
op.add_option( '-p', '--password', dest='password', action='store', help='Password to use for switch login', type='string')
op.add_option( '-i', '--ip', dest='hosts', action='store', help='list of host IP addresses, where to send reload', type='string')
opts, _ = op.parse_args()

#
# User, passwords and method to connect to eAPI on switches
#
EAPI_USERNAME = opts.user
EAPI_PASSWORD = opts.password
EAPI_ENABLE_PASSWORD = ''
EAPI_METHOD = 'https'


#
# Create a list with IPs from the command line option "-i, --ip"
#
hosts = opts.hosts
iplist = hosts.split()

#
# Itereate through the iplist, i.e. iterate through switches
# and collect hostname. If MAC address is found on switch print
# the MAC address and what interface where it was seen
#
for ip in iplist :

 switch = Server( '%s://%s:%s@%s/command-api' % ( EAPI_METHOD, EAPI_USERNAME, EAPI_PASSWORD, ip ) )
 response = switch.runCmds(1, ["reload force"])
