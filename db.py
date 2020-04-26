"""
DB
"""

import logger as lg
import sqlite3
import func as fx

def init():
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row
    return conn


def logData(table, ip, mac, seq, tm, scn, binValue, category):
    db = init()
    cursor = db.cursor()

    cursor.execute('insert into ' + table + '(ip, mac, seq, time, scenario, bin, category) values(?, ?, ?, ?, ?, ?, ?)', (ip, mac, seq, tm, scn, binValue, category))
    db.commit()
    lg.success('Added data to {}: {} <==> {}'.format(table, scn, binValue))


def getTableScenarioCategory(table, scenario, category):
    db = init()
    cursor = db.cursor()
    cursor.execute('select * from ' + table + ' where scenario=? and category=? order by id asc', (scenario, category))
    return cursor.fetchall()

def getTableScenarioCategorySeq(table, scenario, category, seq):
    db = init()
    cursor = db.cursor()
    cursor.execute('select * from ' + table + ' where scenario=? and category=? and seq=? order by id asc', (scenario, category, seq))
    return cursor.fetchall()
