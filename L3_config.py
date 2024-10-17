#!/usr/bin/env python

# Import the pyeapi library
import pyeapi

# Open a session with leaf1-DC1. The script will find .eapi.conf and reference the credentials automatically

connect = pyeapi.connect_to("leaf1-DC1")

# "Create" sets the port as a Layer 3 port (no switchport)

connect.api("ipinterfaces").create('Ethernet4')

# Set Ethernet4 for the IP address of 4.4.4.4 and put the result into the variable (boolean) result

result = connect.api("ipinterfaces").set_address('Ethernet4','4.4.4.4/24')

# This is just very basic error handling here, it gives a yes or no answer depending on whether a "200 OK" response was given, or another error was occurred.

if result == True:
    print("Completed!")
if result == False:
    print("Error!")
