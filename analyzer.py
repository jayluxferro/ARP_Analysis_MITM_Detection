"""
Author: Jay
Date:   20th April, 2020
Packet analyzer
"""
import logger as lg
from scapy.all import *
import socketio
from pprint import pformat
import func as fx
import db
import time

sio = socketio.Client()

def usage():
    print('Usage: python {} <interface>'.format(sys.argv[0]))
    sys.exit(1)

def packetHandler(pkt):
    if pkt.haslayer(ARP) and pkt.haslayer(Padding) and pkt.getlayer(Padding).load != fx.defaultPadding and pkt.getlayer(ARP).op == 2:
        lg.default(pformat(pkt))
        arp = pkt.getlayer(ARP)
        ip = arp.psrc
        mac = arp.hwsrc
        tm = time.time()
        padding = pkt.getlayer(Padding)
        decodedPadding = fx.decodePadding(padding.load)
        seq = decodedPadding[1]
        scn = decodedPadding[0]
        binValue = decodedPadding[2]
        # log data
        db.logData('incoming', ip, mac, seq, tm, scn, binValue)
        print('')

# entry
if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()

    # connect to rpc
    sio.connect('http://{}:{}'.format(fx.network_config['host'], fx.network_config['port']))

    # send burst ARP request packets
    sio.emit('burst', None)

    # sniff for packets
    while True:
        sniff(iface=sys.argv[1], count=1, prn=packetHandler)
