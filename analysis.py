#!/usr/bin/python3

"""
Data Analysis
"""

import func as fx
import db
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# displaying a sample MLS sequence and the RTT
binValue = []
RTT = []

for data in db.getTableScenarioCategory('incoming', fx.iterations, 1):
    for data2 in db.getTableScenarioCategorySeq('outgoing', data['scenario'], 1, data['seq']):
        binValue.append(data2['bin'])
        RTT.append(data['time'] - data2['time'])
x = np.linspace(1, len(binValue), len(binValue))

fig, ax1 = plt.subplots()
ax1.step(x, binValue)
ax1.set_ylabel('Amplitude')
ax1.set_xlabel('Sequence')
ax1.tick_params(axis='y', labelcolor='steelblue')
ax1.legend(['MLS'])

ax2 = ax1.twinx()
ax2.plot(x, RTT, '-ro')
ax2.set_ylabel('Round Trip Time (s)')
ax2.tick_params(axis='y', labelcolor='r')
ax2.legend(['RTT'])
ax2.set_xticks(np.arange(len(x) + 1))
#ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
fig.tight_layout()
plt.grid(True, axis='both')
plt.show()
