#!/usr/bin/python

"""
Custom ARP Reply
"""

from scapy.all import *
import sys
import logger as lg
from pprint import pformat
import func as fx

def usage():
    print('[-] Usage: python {} <interface> <macAddress>'.format(sys.argv[0]))
    sys.exit()


def packetHandler(pkt):
    global mac
    global iface

    if pkt.haslayer(ARP) and pkt.haslayer(Padding) and pkt.getlayer(Padding).load != fx.defaultPadding:
        lg.warning(pformat(pkt))
        print('')
        # replying to request
        paddingPayload = pkt.getlayer(Padding)
        ether = pkt.getlayer(Ether)
        arp = pkt.getlayer(ARP)
        # arpPacket(srcIP, srcMac, dstIP, dstMac, opCode, payload):
        # reversing dst -> src
        """
        >>> ls(Ether)                                                       
            dst        : DestMACField                        = (None)
            src        : SourceMACField                      = (None)
            type       : XShortEnumField                     = (36864)
        >>> ls(ARP)                                                         
            hwtype     : XShortField                         = (1)
            ptype      : XShortEnumField                     = (2048)
            hwlen      : FieldLenField                       = (None)
            plen       : FieldLenField                       = (None)
            op         : ShortEnumField                      = (1)
            hwsrc      : MultipleTypeField                   = (None)
            psrc       : MultipleTypeField                   = (None)
            hwdst      : MultipleTypeField                   = (None)
            pdst       : MultipleTypeField                   = (None)
        """
        newPkt = fx.arpPacket(arp.pdst, mac, arp.psrc, arp.hwsrc, 2, paddingPayload.load)
        fx.sendPacket(iface, newPkt)
        lg.success(pformat(newPkt))
        print('')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()

    global mac
    global iface
    
    iface = sys.argv[1]
    mac = sys.argv[2]

    # sniff for packets
    lg.default('[-] Listening for packets')
    while True:
        sniff(iface=sys.argv[1], count=1, prn=packetHandler)
