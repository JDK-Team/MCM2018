
from data_retrival.readcsv import readcsv
import numpy as np

csv = readcsv('data/Power_Language_Index.csv')
p = np.array(csv)[:,1].astype(float)

def influence(region):
    v = (region.L1 + region.L2) / region.population

    infl = np.multiply(v,p)
    
    return infl / np.sum(infl)
