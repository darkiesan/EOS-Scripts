#!/usr/bin/python

from jsonrpclib import Server
import sys

EAPI_USERNAME = 'cvpadmin'
EAPI_PASSWORD = 'pzkpw51B'
EAPI_ENABLE_PASSWORD = ''
EAPI_METHOD = 'http'
ip = sys.argv[1]
interface = sys.argv[2]

switch = Server( '%s://%s:%s@%s/command-api' % ( EAPI_METHOD, EAPI_USERNAME, EAPI_PASSWORD, ip ) )
response = switch.runCmds(1, ["show interfaces "+interface])

print response[0]["interfaces"][interface]["interfaceCounters"]["outUcastPkts"]
