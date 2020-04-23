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

sio = socketio.Client()

def usage():
    print('Usage: python {} <interface>'.format(sys.argv[0]))
    sys.exit(1)

def packetHandler(pkt):
    if pkt.haslayer(ARP):
        lg.default(pformat(pkt))
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
