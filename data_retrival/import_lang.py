
from data_retrival.readcsv import readcsv

import numpy as np

import logging

def lang_data(filename):
    lang_table = readcsv('data/' + filename)
    lang_data = np.array(lang_table)[1:,1:]
    lang_data[lang_data==''] = '0'
    return lang_data.astype(float)

def lang_names(filename):
    lang_table = np.array(readcsv('data/' + filename))
    return lang_table[1:,0]

