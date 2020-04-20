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
