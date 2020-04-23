"""
Author: Jay
IPC
"""
import socketio
import eventlet
import sys
import logger as lg
import func as fx
import db
from time import sleep

# usage
def usage():
    print('Usage: python {} <interface> <node IP> <scenario>'.format(sys.argv[0]))
    sys.exit(1)

## socket defaults
sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': '../index.html'}
})



# send burst of ARP request packets
def sendBurst():
    global dstIP
    global scenario
    global iface

    for _ in fx.seqNumbers:
        seq = 1
        print('')
        lg.default('[-] Starting {}'.format(_))
        sleep(5)
        for binValue in fx.genMLS():
            # send arp probe request
            pkt = fx.arpPacket(fx.network_config['ip'], fx.network_config['mac'], dstIP, fx.network_config['broadcast'], 1, fx.paddingPayload(seq, binValue))
            fx.sendPacket(iface, pkt)
            lg.warning('[-] Sending ARP probe request packet')
            seq += 1

# events
@sio.on('burst')
def burst(data):
    sendBurst()

@sio.on('connect')
def connect(sid, environ):
    lg.success('Client socket opened => {}'.format(sid))

@sio.on('disconnect')
def disconnect(sid):
    lg.error('Client socket closed => {}'.format(sid))

# daemon
if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage()
    global iface
    global dstIP
    global scenario
    dstIP = sys.argv[2]
    scenario = int(sys.argv[3])
    iface = sys.argv[1]

    eventlet.wsgi.server(eventlet.listen((fx.network_config['host'], fx.network_config['port'])), app)
