#!/usr/bin/python
'''
Sniffer command-line.

Usage:
python mysniff_cmd SELECTION [OPTIONS]

OPTIONS
 -s / --selection=DEV
   The device selected, chosen from the list:
    - gold
    - myphantom
    - bc127
 -h / --help
    Print this help
 -t / --time=TIME
    Select a duration
'''

import ble_sniffer_core as sniff
import sys
import getopt

try:
    opts, args = getopt.getopt(sys.argv[1:], "ht:s:", ["selection=", "help", "time="])
except getopt.GetoptError:
    print('Getopt error')

device_sel = None
device_addr = None

for opt, arg in opts:
    if opt in ["-h", "--help"]:
        print(__doc__)
        sys.exit()
    elif opt in ["-t", "--time="]:
        print("Time selected %d seconds"%arg)
        time = arg
    elif opt in ["-s", "--selection="]:
        print("Selected device %s"%arg)
        device_sel = arg

if device_sel == "gold":
    device_addr = [0x20, 0xFA, 0xBB, 0x03, 0xE7, 0xA5, False]
elif device_sel == "myphantom":
    device_addr = [0x0A, 0x9D, 0x02, 0xBB, 0xFA, 0x20, False]
elif device_sel == "bc127":
    device_addr = [0xC7, 0xFD, 0xBE, 0xF4, 0xFA, 0xD7, False]
else:
    print("No device selection, running scan for device choice.")

if device_addr != None:
    sniff.setup(device_addr)
    sniff.loop()
else:
    device_addr = sniff.select_dev()
    sniff.setup(device_addr)
    sniff.loop()
