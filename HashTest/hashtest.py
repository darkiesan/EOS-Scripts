#!/usr/bin/python

from jsonrpclib import Server
from scapy.all import send,IP,UDP
from random import randint
import sqlite3

#
# Set scriptwide constants
#
PAYLOAD = "TEST"
SPORT = 32000
DPORT = 514

#
# Read config file and populate variables needed
#

myfile = open('hashtest.cfg','r')
file_contents = myfile.read().splitlines()
myfile.close()

for element in file_contents:
 cfglist = element.split('=') 

 if cfglist[0] == 'switchip':
  switchIP = cfglist[1]

 if cfglist[0] == 'switchusername':
  switchUsername = cfglist[1]

 if cfglist[0] == 'switchpassword':
  switchPassword = cfglist[1]

 if cfglist[0] == 'switcheapiprotocol':
  switchEAPIProtocol = cfglist[1]

 if cfglist[0] == 'switchportchannel':
  switchPortchannel = cfglist[1].split(',')

#
# Read IP range used for src and dst in tes
#

myfile = open('iprange.txt','r')
file_contents = myfile.read().splitlines()
myfile.close()

counter = 1
sourceIPs = []
destinationIPs = []
for element in file_contents:
 sourceIPs.insert(counter, element)
 destinationIPs.insert(counter, element)
 counter = counter + 1

myfile = open('portrange.txt','r')
file_contents = myfile.read().splitlines()
myfile.close()

counter = 1
srcPorts = []
dstPorts = []
for element in file_contents:
 srcPorts.insert(counter, element)
 dstPorts.insert(counter, element)
 counter = counter + 1

#
# From each srcIP send a packet to each dstIP. Before it is sent, clear counters on all member interfaces of the PortChannel. 
# After packet is sent, check counters on member interfaces of the Portchannel to see which interface the hash sent the packout
# out of. Also prepare a result database (sqlite3) with the filename taken from command line
#

result_db = sqlite3.connect('result.db')
cursor = result_db.cursor()
cursor.execute('CREATE TABLE output (srcIP text, srcPort text, dstIP text, dstPort text, outInterface text)')

for srcIP in sourceIPs:
 for dstIP in destinationIPs:
   for srcPort in srcPorts:
    for dstPort in dstPorts:

      for interface in switchPortchannel:
        switch = Server( '%s://%s:%s@%s/command-api' % ( switchEAPIProtocol, switchUsername, switchPassword, switchIP ) )
        response = switch.runCmds(1, ["enable", "clear counters "+interface])

      send(IP(src=srcIP, dst=dstIP) / UDP(sport=SPORT, dport=DPORT) / PAYLOAD, verbose=False)

      for interface in switchPortchannel:
       switch = Server( '%s://%s:%s@%s/command-api' % ( switchEAPIProtocol, switchUsername, switchPassword, switchIP ) )
       response = switch.runCmds(1, ["show interfaces "+interface])
       intCounter = response[0]["interfaces"][interface]["interfaceCounters"]["outUcastPkts"]

      outInterface = 'Loopback0'
      if intCounter > 0:
        outInterface = interface

      print 'srcIP %s srcPort %s dstIP %s dstPort %s egress %s' % ( srcIP, srcPort, dstIP, dstPort, outInterface)
      cursor.execute("insert INTO output VALUES (?, ?, ?, ?, ?)", (srcIP, srcPort, dstIP, dstPort, outInterface))
      result_db.commit()

result_db.close()
print "All packets sent and recorded in result.db sqlite3 file."
