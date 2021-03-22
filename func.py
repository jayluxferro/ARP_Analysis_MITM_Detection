"""
Author: Jay
Date:   20th April, 2020
Default Functions
"""

from scipy.signal import max_len_seq as mls
from scapy.all import *
import cmpp
import numpy as np
from pandas import DataFrame as DF
from sklearn.metrics import classification_report

network_config = {'host': '127.0.0.1', 'port': 5000, 'ip': '172.24.1.1', 'mac': 'c4:e9:84:df:3c:98', 'default_mac': '00:00:00:00:00:00', 'broadcast': 'ff:ff:ff:ff:ff:ff'}
paddingLength = 18
padding = '\x00'
defaultPadding = padding * paddingLength
iterations = 200
seqNumbers = [ i + 1 for i in range(iterations) ]
binaryByteLen = 1
seqByteLen = 4
getHex = {'00': '\x00', '01': '\x01', '10': '\x10', '11': '\x11'}
invHex = {'\x00': '00', '\x01': '01', '\x10': '10', '\x11': '11'}
numberOfBits = 16
dataset = 'data.csv'

def metricReport(y_true, y_pred, file_name):
    clsf_report = DF(classification_report(y_true=y_true, y_pred=y_pred, output_dict=True)).transpose()
    clsf_report.to_latex(file_name, index= True)

def plot_cm(cm, title='Confusion Matrix', display_labels=None, output_file=None):
    cmap = 'PuRd'
    cm = np.array(cm)
    cmpp.pretty_plot_confusion_matrix(DF(cm, index=display_labels, columns=display_labels), cmap=cmap, title=title, output_file=output_file)

def genMLS(nbits=numberOfBits, length=iterations):
    return  mls(nbits=numberOfBits, length=length)[0] # returns a numpy array

def arpPacket(srcIP, srcMac, dstIP, dstMac, opCode, payload):
    """
    ###[ Ethernet ]###
      dst= 00:0c:29:4c:d2:a5
      src= 00:50:56:f5:3d:32
      type= ARP
    ###[ ARP ]###
     hwtype= 0x1
     ptype= IPv4
     hwlen= 6
     plen= 4
     op= is-at
     hwsrc= 00:50:56:f5:3d:32
     psrc= 172.16.239.2
     hwdst= 00:0c:29:4c:d2:a5
     pdst= 172.16.239.133
    ###[ Padding ]###
        load= '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    """
    return Ether(dst=dstMac, src=srcMac)/ARP(hwlen=6, plen=4, op=opCode, hwsrc=srcMac, psrc=srcIP, hwdst=dstMac, pdst=dstIP)/Padding(load=payload)


def b2h(binValue, length): # inputs : binary, and integer
    binValue = [ i for i in binValue.split('0b')[1] ]
    if len(binValue) % 2 == 1:
        binValue.insert(0, '0') # just to prepend 0 to make it even length

    # to get something like: 00 11 10 from 001110
    newBinValue = []
    holder = ''
    counter = 0
    for i in binValue:
        if counter == 0:
            holder = i
        else:
            if counter % 2 == 1:
                holder += i
                newBinValue.append(getHex[holder])
            else:
                holder = i
        counter += 1
    if len(newBinValue) < length:
        # prepend '00'
        for _ in range(length - len(newBinValue)):
            newBinValue.insert(0, padding)

    # now change to  eg. '\x00\x01'
    return ''.join(newBinValue)

def paddingPayload(scenario, seq, binary, category): # inputs are expected to be integers
    # first part of the payload
    extraPadding = padding * (paddingLength - binaryByteLen - (3 * seqByteLen))

    # scenario
    scenario = b2h(bin(scenario), seqByteLen)

    # sequence 
    seq = b2h(bin(seq), seqByteLen)

    # binary
    binary = b2h(bin(binary), binaryByteLen)

    # category
    category = b2h(bin(category), seqByteLen)

    return extraPadding + category + scenario + seq + binary

def decodePadding(payload):
    payload = [ invHex[i] for i in list(tuple(payload)) ]

    # binValue
    binValue = int(payload[-1])

    # seq
    seq = int(''.join(payload[-5:-1]), 2)

    # scenario
    scenario = int(''.join(payload[-9:-5]), 2)

    # category
    category = int(''.join(payload[-13:-9]), 2)

    return (category, scenario, seq, binValue)

def sendPacket(interface, pkt):
    sendp(pkt, iface=interface) # layer 2
