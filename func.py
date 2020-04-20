"""
Author: Jay
Date:   20th April, 2020
Default Functions
"""

from scipy.signal import max_len_seq as mls

network_config = {'host': '127.0.0.1', 'port': 5000}

def genMLS(numberOfBits=1):
    return  mls(numberOfBits)[0] # returns a numpy array
