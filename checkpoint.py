#!/usr/bin/env python

from jsonrpclib import Server
import argparse

#
# Define command line options for argparse
#

usage = 'usage: %prog [options]'

ap = argparse.ArgumentParser()
ap.add_argument(
    "-u",
    "--username",
    dest="username",
    action="store",
    required=True,
    help="EOS username",
)

ap.add_argument(
    "-i",
    "--ipaddresscvpusername",
    dest="ipaddress",
    action="store",
    required=True,
    help="EOS device IP address",
)

ap.add_argument(
    "-p",
    "--password",
    dest="password",
    action="store",
    required=True,
    help="EOS password",
)

opts = ap.parse_args()

ip = opts.ipaddress
user = opts.username
password = opts.password

switch = Server( '%s://%s:%s@%s/command-api' % ( 'http', user, password, ip ) )
result = switch.runCmds(1, ['enable' , 'copy running-config backup-config'])
print result
