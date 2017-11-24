#!/usr/bin/python

from scapy.all import send,IP,UDP

DHOST = '192.168.200.214'
DPORT = 514
SHOST = '10.10.10.10'
SPORT = 32000
PAYLOAD = 'test'

send(IP(src=SHOST, dst=DHOST) / UDP(sport=SPORT, dport=DPORT) / PAYLOAD)

print 'Source IP: %s, Source port: %s, Destination IP %s, Destination port: %s' % ( SHOST, SPORT, DHOST, DPORT )

