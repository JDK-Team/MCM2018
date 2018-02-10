
def death(world, n):
    region = world.regions[n]

    thousands = region.population / 1000
    region.population -= thousands * region.deathrate

    thousandsL1 = region.L1 / 1000
    region.L1 -= thousandsL1 * region.deathrate
    
    thousandsL2 = region.L2 / 1000
    region.L2 -= thousandsL2 * region.deathrate
