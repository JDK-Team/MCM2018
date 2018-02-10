
from data_retrival.readcsv import readcsv
import numpy as np


def scalar_data(filename, year):
    data_table = readcsv('data/' + filename)
    title_row = data_table[0]
    col = title_row.index('X' + str(year))
    pop_matrix = np.array(data_table[1:])
    pops = pop_matrix[:,col]
    return np.array(pops).astype(float)

def identifiers():
    pop_table = readcsv('data/regionPops.csv')
    pop_matrix = np.array(pop_table[1:])
    ids = pop_matrix[:,1]
    
    return ids
