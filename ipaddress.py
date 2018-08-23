#!/usr/bin/python

import jsonrpclib
import optparse

EAPI_USERNAME = ''
EAPI_PASSWORD = ''
EAPI_ENABLE_PASSWORD = ''
EAPI_METHOD = 'http'

usage = 'usage: %prog [options]'
op = optparse.OptionParser(usage=usage)
op.add_option( '-n', '--host', dest='host', action='store', help='IP addresses of host to connect to', type='string')
op.add_option( '-i', '--ip', dest='address', action='store', help='IP addresses to set on Interface', type='string')
op.add_option( '-t', '--interface', dest='interface', action='store', help='interface to configure', type='string')
opts, _ = op.parse_args()

host = opts.host
address = opts.address
interface = opts.interface

switch = jsonrpclib.Server( '%s://%s:%s@%s/command-api' % ( EAPI_METHOD, EAPI_USERNAME, EAPI_PASSWORD, host ) )
response = switch.runCmds(1, ["enable", "configure", "interface " + interface, "ip address " + address])
