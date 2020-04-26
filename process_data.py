#!/usr/bin/python

"""
Data Analysis
"""

import func as fx
import db
import logger as lg
import matplotlib.pyplot as plt
import numpy as np

categories = [1, 2]
normal = []
mitm = []

lg.default('[-] Generating dataset...')
fileHandler = open(fx.dataset, 'w')
details = 'RTT,Category\n'
for iteration in fx.seqNumbers:
    for category in categories:
        for data in db.getTableScenarioCategory('incoming', iteration, category):
            for data2 in db.getTableScenarioCategorySeq('outgoing', data['scenario'], category, data['seq']):
                ctg = category
                rtt = np.abs(data['time'] - data2['time'])
                details += '{},{}\n'.format(rtt, ctg-1)
                if ctg == 1:
                    normal.append(rtt)
                else:
                    mitm.append(rtt)

fileHandler.write(details)
fileHandler.close()
lg.success('[+] Dataset generated')

# analyzing the points
plt.figure()
plt.plot(np.linspace(1, len(normal), len(normal)), normal, '*')
plt.plot(np.linspace(1, len(mitm), len(mitm)), mitm, 'o')
plt.xlabel('Data Points')
plt.ylabel('RTT')
plt.legend(['Normal', 'MITM'])
plt.show()
