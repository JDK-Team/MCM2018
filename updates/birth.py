import logging

def birth(world, subs, n):
    region = world.regions[n]
    
    #logging.debug(region.birthrate)

    thousands = region.population / 1000
    region.population += (thousands * region.birthrate) / subs

    thousandsL1 = region.L1 / 1000
    region.L1 += (thousandsL1 * region.birthrate) / subs 
    
    thousandsL2 = region.L2 / 1000
    region.L2 += (thousandsL2 * region.birthrate) / subs



# birth rate number is - births per thousand people.
