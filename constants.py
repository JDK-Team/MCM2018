
#NUM_LANGUAGES = 26
#NUM_REGIONS = 20

#LANGUAGE_NAMES = ["English", "Mandarin", "Spanish"]

#REGION_NAMES = ["USA", "Mexico", "China"]


# region attributes

#REGION_POPULATIONS = [320,127,1379]
#REGION_BIRTHRATES = [1.03,1.05,1.00]
#REGION_DEATHRATES = [0.99,0.99,0.99]
#REGION_L1 = [[280, 0, 40], 
#             [10, 0, 117], 
#             [0, 1379, 0]] # size = NUM_LANGUAGES x NUM_REGIONS 
#REGION_L2 = [[30, 0, 80],
#             [50, 0, 0],
#             [300, 0, 0]]

# edge attributes

#EDGE_IMMIGRATION = [[0,.5,0],
#                    [1,0,0],
#                    [.5,0,0]] # SIZE = NUM_REGIONS x NUM_REGIONS

from data_retrival.import_mig import mig_data
from data_retrival.import_pop import scalar_data, identifiers

import numpy as np

REGION_NAMES = identifiers()
LANGUAGE_NAMES = ['Name' + str(i) for i in range(0,26)]

NUM_REGIONS = len(REGION_NAMES)
NUM_LANGUGAGES = 26

REGION_POPULATIONS = scalar_data('regionPops.csv', 2010) 
REGION_BIRTHRATES = scalar_data('r_birthRate.csv', 2010)
REGION_DEATHRATES = scalar_data('r_deathRate.csv', 2010)

EDGE_IMMIGRATION = mig_data('r_migration2010_withk.csv')

REGION_L1 = np.zeros((NUM_REGIONS,26))
REGION_L2 = np.zeros((NUM_REGIONS,26))
