
from Struct import Struct
import constants
import numpy as np
import logging

def create_regions(names, pops, L1s, L2s, brates, drates):
    regions = [Struct(name=n) for n in names]
    n = len(regions)
    logging.debug(len(brates))
    for i in range(0,n):
        regions[i].population = pops[i]
        regions[i].L1 = L1s[i,:]
        regions[i].L2 = L1s[i,:]
        regions[i].birthrate = brates[i]
        regions[i].deathrate = drates[i]
    return regions

def create_languages(names):
    languages = [Struct(name=n) for n in names]
    return languages

def create_edges(immigrations):
    edges = [[Struct() for im in row] for row in immigrations]
    n = len(edges) # must be square
    for i in range(0,n):
        for j in range(0,n): # must be square
            edges[i][j].immigration = immigrations[i][j]
            #edges[i][j].regionalImpact = regional
    return edges

def create_from_constants():
    regs = create_regions(constants.REGION_NAMES,
                          constants.REGION_POPULATIONS,
                          constants.REGION_L1,
                          constants.REGION_L2,
                          constants.REGION_BIRTHRATES,
                          constants.REGION_DEATHRATES)
    langs = create_languages(constants.LANGUAGE_NAMES)
    edges = create_edges(constants.EDGE_IMMIGRATION)
    return Struct(regions=regs,languages=langs,edges=edges)

