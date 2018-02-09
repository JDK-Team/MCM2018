
from Struct import Struct
import constants

def create_regions(names, pops, L1s, L2s):
    regions = [Struct(name=n) for n in names]
    n = len(regions)
    for i in range(0,n):
        regions[i].population = pops[i]
        regions[i].L1 = L1s[i]
        regions[i].L2 = L2s[i]
    return regions

def create_languages(names):
    languages = [Struct(name=n) for n in names]
    return languages

def create_edges(immigrations):
    edges = [[Struct(imconst=im) for im in row] for row in immigrations]
    return edges

def create_from_constants():
    regs = create_regions(constants.REGION_NAMES,
                          constants.REGION_POPULATIONS,
                          constants.REGION_L1,
                          cosntants.REGION_L2)
    langs = create_languages(constants.LANGUAGE_NAMES)
    edges = create_edges(constants.EDGE_IMMIGRATION)
    return Struct(regions=regs,languages=langs,edges=edges)

