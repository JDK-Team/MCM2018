
from data_retrival.readcsv import readcsv
import numpy as np

pop_table = readcsv('data/regionPops.csv')

title_row = pop_table[0]

pop_matrix = np.array(pop_table[1:])

ids = pop_matrix[:,1]

def pop_data(year):
    col = title_row.index('X' + str(year))
    pops = pop_matrix[:,col]
    return np.array([ids, pops])

def identifiers():
    return ids
