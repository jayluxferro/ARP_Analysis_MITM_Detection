#!/usr/bin/python3

"""
Data Analysis
"""

import func as fx
import db
import logger as lg

categories = [1, 2]

lg.default('[-] Generating dataset...')
fileHandler = open(fx.dataset, 'w')
details = 'RTT,Category\n'
for iteration in fx.seqNumbers:
    for category in categories:
        for data in db.getTableScenarioCategory('incoming', iteration, category):
            for data2 in db.getTableScenarioCategorySeq('outgoing', data['scenario'], category, data['seq']):
                ctg = category
                rtt = data['time'] - data2['time']
                details += '{},{}\n'.format(rtt, ctg)

fileHandler.write(details)
fileHandler.close()
lg.success('[+] Dataset generated')
