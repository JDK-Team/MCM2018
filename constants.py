
NUM_LANGUAGES = 26
NUM_REGIONS = 20

LANGUAGE_NAMES = ["English", "Mandarin", "Spanish"]

REGION_NAMES = ["USA", "Mexico", "China"]


# region attributes

REGION_POPULATIONS = [320,127,1379]
REGION_BIRTHRATES = [1.03,1.05,1.00]
REGION_DEATHRATES = [0.99,0.99,0.99]
REGION_L1 = [[280, 0, 40], 
             [10, 0, 117], 
             [0, 1379, 0]] # size = NUM_LANGUAGES x NUM_REGIONS 
REGION_L2 = [[30, 0, 80],
             [50, 0, 0],
             [300, 0, 0]]

# edge attributes

EDGE_IMMIGRATION = [[0,.5,0],
                    [1,0,0],
                    [.5,0,0]] # SIZE = NUM_REGIONS x NUM_REGIONS
