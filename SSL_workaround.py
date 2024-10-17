#!/usr/bin/env python

#
# Import modules
#
from jsonrpclib import Server
import ssl

# Use TLSv1.2
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.minimum_version = ssl.TLSVersion.TLSv1_2
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Using the EOS default ciphers
context.set_ciphers('AES256-SHA:DHE-RSA-AES256-SHA:AES128-SHA:DHE-RSA-AES128-SHA')