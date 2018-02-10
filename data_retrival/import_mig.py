
from data_retrival.readcsv import readcsv
import numpy as np
from data_retrival.import_pop import identifiers
import logging

# migrations go FROM row TO column

def mig_data(filename):
    mig_table = readcsv('data/' + filename)
    title_row = mig_table[0]
    mig_data = np.array(mig_table[1:])
    logging.debug(mig_data)
    k_vals = mig_data[:,0].astype(np.float)
    logging.debug(k_vals)
    n = len(identifiers())
    logging.debug('{} {}'.format(n, n*n))
    logging.debug(len(k_vals))
    if not n*n == len(k_vals):
        logging.error("mismatched dimensions in k values")
    edge_matrix = np.transpose(np.reshape(k_vals,(n,n)))
    logging.debug(edge_matrix.shape)
    return edge_matrix


