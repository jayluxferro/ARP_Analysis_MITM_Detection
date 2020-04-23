#!/usr/bin/python

"""
Custom ARP Reply
"""

from scapy.all import *
import sys
import logger as lg
from pprint import pformat

def usage():
    print('[-] Usage: python {} <interface>'.format(sys.argv[0]))
    sys.exit()


def packetHandler(pkt):
    if pkt.haslayer(ARP) and pkt.haslayer(Padding):
        lg.success(pformat(pkt))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()


    # sniff for packets
    lg.default('[-] Listening for packets')
    while True:
        sniff(iface=sys.argv[1], count=1, prn=packetHandler)
