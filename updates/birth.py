import logging

def birth(world, n):
    region = world.regions[n]

    thousands = region.population / 1000
    region.population += thousands * region.birthrate

    thousandsL1 = region.L1 / 1000
    region.L1 += thousandsL1 * region.birthrate 
    
    thousandsL2 = region.L2 / 1000
    region.L2 = thousandsL2 * region.birthrate



# birth rate number is - births per thousand people.
