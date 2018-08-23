#!/usr/bin/env python

from jsonrpclib import Server
import optparse

EAPI_USERNAME = 'myuser'
EAPI_PASSWORD = 'mypass'
EAPI_ENABLE_PASSWORD = ''
EAPI_METHOD = 'http'

#
# Define available options on the command line to restart-streaming.py
#
usage = 'usage: %prog [options]'
op = optparse.OptionParser(usage=usage)
op.add_option( '-u', '--username', dest='username', action='store', help='Username to use on switches', type='string')
op.add_option( '-p', '--password', dest='password', action='store', help='Password to use on switches', type='string')
op.add_option( '-i', '--ipaddresses', dest='ipaddresses', action='store', help='List of IP addresses to switches', type='string')
opts, _ = op.parse_args()

username = opts.username
password = opts.password
ipaddresses = opts.ipaddresses
iplist = ipaddresses.split()

EAPI_ENABLE_PASSWORD = ''
EAPI_METHOD = 'http'

for ip in iplist:
	switch = Server( '%s://%s:%s@%s/command-api' % ( EAPI_METHOD, username, password, ip ) )
	response = switch.runCmds(1, ["enable", "daemon TerminAttr", "shutdown"+])
	response = switch.runCmds(1, ["enable", "daemon TerminAttr", "no shutdown"+])
