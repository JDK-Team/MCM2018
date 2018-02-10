
from data_retrival.readcsv import readcsv

import numpy as np

import logging

def lang_data(filename):
    lang_table = readcsv('data/' + filename)
    lang_data = np.array(lang_table)[1:,1:]
    return lang_data.astype(float)
