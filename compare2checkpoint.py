#!/usr/bin/python

from os import system
import sys
import diffios

base = sys.argv[1]
compare = sys.argv[2]

if base == "running-config":
    system("Cli -p 15 -c 'show run > flash:showrun.conf'")
    baseline = "/mnt/flash/showrun.conf"
elif base == "startup-config":
    baseline = "/mnt/flash/startup-config"
else:
    baseline = "/mnt/flash/.checkpoints/" + base

comparison = "/mnt/flash/.checkpoints/" + compare

diff = diffios.Compare(baseline, comparison)

print(diff.delta())
