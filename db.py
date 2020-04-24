"""
DB
"""

import logger as lg
import sqlite3
import func as fx

def init():
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row
    return con


def logData(table, ip, mac, seq, tm, scn, binValue):
    db = init()
    cursor = db.cursor()
    cursor.execute('insert into ' + table + '(ip, mac, seq, time, scenario, bin) values(?, ?, ?, ?, ?, ?)', (ip, mac, seq, tm, scn, binValue))
    db.commit()
    lg.success('Added data to {}: {} <==> {}'.format(table, scn, binValue))
